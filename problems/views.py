from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

from problems.models import Problem, Session, Important, PersonType, Survey

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

def important(request):
    if request.POST:
        selected_problems = []
        # check for existing session
        session = Session()
        session.save()
        for problem in [x for x in request.POST if 'problem' in x ]:
            try:
                pid = problem.split('-')[1]
                prob = Problem.objects.get(id=pid)
                selected_problems.append(prob)
            except:
                continue
        for problem in selected_problems:
            imp = Important(
                problem=problem,
                session=session,
                )
            imp.save()
        return HttpResponseRedirect(reverse(thanks))
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
        help_text= 'Enter the date in YYYY format',
        )
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse(thanks)
        self.helper.add_input(Submit('submit', 'Submit'))
    

def thanks(request):
    survey_form = SurveyForm()
    if request.POST:
        survey_form = SurveyForm(request.POST)
        if survey_form.is_valid():
            survey = Survey()
            survey.birth_year = survey_form.cleaned_data['birth_year']
            survey.save()
            for t in survey_form.cleaned_data['person_types']:
                ty, created = PersonType.objects.get_or_create(name=t)
                survey.person_types.add(ty)

    return render_to_response('problems/thanks.html',{
        'form':survey_form,
        },context_instance=RequestContext(request))