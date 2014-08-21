from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

import json

from django.contrib.auth.models import User
from problems.models import Problem, Session, Important, PersonType, Survey, Suggestion

from problems.forms import SuggestionForm

from django.contrib import messages

from django.core.mail import send_mail

def pick(request):
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
            if request.is_ajax():
                return HttpResponse(json.dumps({
                    'content':"Something",
                    }),
                    mimetype='application/json',
                )
            return HttpResponseRedirect(reverse(order))
        messages.add_message(request, messages.ERROR, 'Either skip this message, or select a problem.')
    if request.is_ajax():
        return HttpResponse(json.dumps({
                'content':"Something",
                }),
            mimetype='application/json',
            )
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

