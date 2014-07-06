from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

from django.contrib.auth.models import User
from problems.models import Problem, Session, Important, PersonType, Survey, Suggestion

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib import messages

def important(request):
    session = False
    if 'session_key' in request.session:
        session = Session.objects.get_or_create(key=request.session['session_key'])

    if request.POST:
        selected_problems = []
        # check for existing session
        for problem in [x for x in request.POST if 'problem' in x ]:
            try:
                pid = problem.split('-')[1]
                prob = Problem.objects.get(id=pid)
                selected_problems.append(prob)
            except:
                continue
        if len(selected_problems) >= 1 or 'skip' in request.POST:
            if not session:
                session = Session()
                session.save()
                request.session['session_key'] = session.key
            for problem in selected_problems:
                imp = Important(
                    problem=problem,
                    session=session,
                    )
                imp.save()
            return HttpResponseRedirect(reverse(thanks))
        messages.add_message(request, messages.ERROR, 'Either skip this message, or select a problem.')
    if session:
        # load problems from last session
        pass
    return render_to_response('problems/page-first.html',{
        'problems':Problem.objects.all(),
        },context_instance=RequestContext(request))

class SurveyForm(forms.Form):
    person_types = forms.MultipleChoiceField(
        label = 'Check every term that best descibe you',
        widget=forms.CheckboxSelectMultiple,
        choices = (
            ('Patient','Patient'),
            ('Medical Provider','Medical Provider'),
            ('Caregiver','Caregiver'),
            ('Designer','Designer'),
            ('Technologist','Technologist'),
            ),
        )
    birth_year = forms.CharField(
        label = 'Enter your birth year',
        help_text= 'Enter the year in YYYY format',
        )
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse(survey)
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        if 'birth_year' not in cleaned_data:
            return cleaned_data
        birth_year = cleaned_data['birth_year']
        if len(birth_year) != 4:
            self._errors['birth_year'] = self.error_class(['Please enter only 4 digits'])
            del cleaned_data['birth_year']
        try:
            birth_year = int(birth_year)
        except:
            self._errors['birth_year'] = self.error_class(['Please enter only numbers'])
            del cleaned_data['birth_year']
        return cleaned_data

class EmailForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse(email)
        self.helper.add_input(Submit('submit', 'Submit'))

def thanks(request):
    if 'session_key' not in request.session:
        return important(request)
    survey_form = SurveyForm()
    email_form = EmailForm()

    return render_to_response('problems/thanks.html',{
        'form':survey_form,
        'email_form':email_form,
        },context_instance=RequestContext(request))

def survey(request):
    if 'session_key' not in request.session:
        return HttpResponseRedirect(reverse(important))
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    form = SurveyForm()
    if request.POST:
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = Survey()
            survey.birth_year = form.cleaned_data['birth_year']
            survey.save()
            for t in form.cleaned_data['person_types']:
                ty, created = PersonType.objects.get_or_create(name=t)
                survey.person_types.add(ty)
    return render_to_response('problems/form.html',{
        'form':form,
        },context_instance=RequestContext(request))

def email(request):
    if 'session_key' not in request.session:
        return HttpResponseRedirect(reverse(important))
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    form = EmailForm()
    if request.POST:
        form = EmailForm(request.POST)
        if form.is_valid():
            user, created = User.objects.get_or_create(username=form.cleaned_data['email'], email=form.cleaned_data['email'])
            session.user = user
            session.save()
            messages.add_message(request,messages.SUCCESS,'Added your email address %s.' % (user.email))
            return HttpResponseRedirect(reverse(thanks))
    return render_to_response('problems/form.html',{
        'form':form,
        },context_instance=RequestContext(request))

class ProblemAddForm(forms.Form):
    description = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ProblemAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse(add)
        self.helper.add_input(Submit('submit', 'Submit'))

def add(request):
    if 'session_key' not in request.session:
        return HttpResponseRedirect(reverse(important))
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    form = ProblemAddForm()
    if request.POST:
        form = ProblemAddForm(request.POST)
        if form.is_valid():
            s = Suggestion(
                description = form.cleaned_data['description'],
                session = session,
                )
            s.save()
            messages.add_message(request, messages.SUCCESS, 'Added your problem suggestion. We will add it to the site soon.')
            return HttpResponseRedirect(reverse(thanks))
    return render_to_response('problems/add.html',{
            'form':form,
            },context_instance=RequestContext(request))    

