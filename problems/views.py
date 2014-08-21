from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from main.views import response

from django.contrib.auth.models import User
from problems.models import Problem, Session, Important, PersonType, Survey, Suggestion

from problems.forms import SuggestionForm

from django.contrib import messages

from django.core.mail import send_mail

def pick(request):
    try:
        session = Session.objects.get(key=request.session['session_key'])
    except:
        return response(request, redirect=reverse('main-home'))

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
            for problem in selected_problems:
                imp = Important(
                    problem=problem,
                    session=session,
                    )
                imp.save()
            return response(request, redirect=reverse('problems-order'))
        messages.add_message(request, messages.ERROR, 'Either skip this message, or select a problem.')
    return response(request,{
        'problems':Problem.objects.all(),
        },
        render='problems/problems-form.html')

def order(request):
    try:
        session = Session.objects.get(key=request.session['session_key'])
    except:
        return response(request, redirect=reverse('main-home'))
    if len(session.problems()) <= 1:
        return response(request, redirect=reverse('suggestion-add'))
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
        return response(request, redirect=reverse('suggestion-add'))
    return response(request,{
        'problems':session.problems(),
        }, render='problems/order.html')


def suggestion(request):
    try:
        session = Session.objects.get(key=request.session['session_key'])
    except:
        return response(request, redirect=reverse('main-home'))
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
            return response(request, redirect=reverse('main-home'))
        if 'skip' in request.POST:
            return response(request, redirect=reverse('main-home'))
    return response(request, {
        'form':form,
        },
        render='problems/suggestions.html',
        )

