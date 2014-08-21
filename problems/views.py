from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

from django.contrib.auth.models import User
from problems.models import Problem, Session, Important, PersonType, Survey, Suggestion

from problems.forms import SuggestionForm, SurveyForm, EmailForm, ProblemAddForm

from django.contrib import messages

from django.core.mail import send_mail

def pick(request):
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
            return HttpResponseRedirect(reverse(order))
        messages.add_message(request, messages.ERROR, 'Either skip this message, or select a problem.')
    if session:
        # load problems from last session
        pass
    return render_to_response('problems/page-first.html',{
        'problems':Problem.objects.all(),
        },context_instance=RequestContext(request))

def order(request):
    try:
        session = Session.objects.get(key=request.session['session_key'])
    except:
        return HttpResponseRedirect(reverse(important))
    if len(session.problems()) <= 1:
        return HttpResponseRedirect(reverse(suggestion))
    if request.POST:
        for problem in [x for x in request.POST if 'problem' in x ]:
            try:
                pid = problem.split('-')[1]
                imp = Important.objects.get(
                    problem__id=pid,
                    session = session,
                    )
                imp.ranking = int(request.POST[problem])
                imp.save()
            except:
                pass
        return HttpResponseRedirect(reverse(suggestion))
    return render_to_response('problems/order.html',{
        'problems':session.problems(),
        }, context_instance=RequestContext(request))


def suggestion(request):
    try:
        session = Session.objects.get(key=request.session['session_key'])
    except:
        return HttpResponseRedirect(reverse(important))
    form = SuggestionForm()
    if request.POST:
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = Suggestion(
                session = session,
                description = form.cleaned_data['description']
                )
            suggestion.save()
            if 'email' in form.cleaned_data['email']:
                session.email_add(form.cleaned_data['email'])
            messages.add_message(request, messages.SUCCESS,'Your suggestion has been saved. We will notify you when it is made public.')
            return HttpResponseRedirect(reverse(thanks))
    return render_to_response('problems/suggestions.html',{
        'form':form,
        }, context_instance=RequestContext(request))

def thanks(request):
    if 'session_key' not in request.session:
        return important(request)
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    
    survey_form = SurveyForm(session=session)
    email_form = EmailForm(session=session)

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
            return HttpResponseRedirect(reverse(thanks))
    return render_to_response('problems/form.html',{
        'form':form,
        },context_instance=RequestContext(request))

def email(request):
    if 'session_key' not in request.session:
        return HttpResponseRedirect(reverse(important))
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    form = EmailForm(session = session)
    if request.POST:
        form = EmailForm(request.POST, session = session)
        if form.is_valid():
            user, created = User.objects.get_or_create(username=form.cleaned_data['email'], email=form.cleaned_data['email'])
            session.user = user
            session.save()
            messages.add_message(request,messages.SUCCESS,'Added your email address %s.' % (user.email))
            send_mail(
                'Your diabetes problems account',
                'You can continue your session at anytime by visiting %s' % (
                    request.build_absolute_uri(reverse(start, kwargs={'session_key':session.key})),
                    ),
                'no-reply@healthdesignby.us',
                [user.email],
                fail_silently=True
                )
            return HttpResponseRedirect(reverse(thanks))
    return render_to_response('problems/form.html',{
        'form':form,
        },context_instance=RequestContext(request))

def start(request, session_key=False):
    if session_key:
        try:
            session = Session.objects.get(key = session_key)
            messages.add(request, messages.SUCCESS,'You session has been started')
            request.session['session_key'] = session_key
        except:
            messages.add(request, messages.ERROR,'Your session doesn\'t exist')
    return HttpResponseRedirect(reverse(thanks))

def end(request):
    try:
        del request.session['session_key']
        messages.add(request,messages.SUCCESS,'Your session has been ended.')
    except:
        pass
    return HttpResponseRedirect(reverse(thanks))

