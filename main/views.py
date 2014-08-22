from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext
from django.contrib import messages

import json

from problems.models import Session
from main.forms import SurveyForm, EmailForm

import django.dispatch
pre_template_render = django.dispatch.Signal(providing_args=["template"])

def response(request, data={}, template="base.html", render=False, error=False, redirect=False):
    for reciver, response in pre_template_render.send(False, template=template):
        if response:
            template = response
    if request.is_ajax():
        if render:
            template = render
    	if template and template != "base.html":
    		content = render_to_string(template, data, context_instance=RequestContext(request))
    		data = {'content':content}
        if redirect:
            data = {'redirect':redirect}
        data['messages'] = []
        for message in messages.get_messages(request):
            data['messages'].append({
                'text':message.message,
                'type':message.tags,
                })
    	return HttpResponse(
    		json.dumps(data),
    		content_type='application/json',
    		)
    if redirect:
        return HttpResponseRedirect(redirect)
    if render:
        content = render_to_string(render, data, context_instance=RequestContext(request))
        data = {'content': content}
    return render_to_response(
    	template,
    	data,
    	context_instance=RequestContext(request)
    	)	

def home(request):
    if 'session_key' not in request.session:
        session = Session()
        session.save()
        request.session['session_key'] = session.key
        return response(request,
            template='home.html',
            )
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    
    survey_form = SurveyForm(session=session)
    email_form = EmailForm(session=session)

    return response(request,
    	data = {
        'form':survey_form,
        'email_form':email_form,
        },
        render='problems/thanks.html',
        )

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
            return response(request, redirect=reverse('main-home'))
    return response(request,
    	render='main/form.html',
    	data = { 'form':form }
    	)

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
            return response(request, redirect=reverse('main-home'))
    return response(request,
    	render='main/form.html',
    	data = { 'form':form }
    	)

def start(request, session_key=False):
    if session_key:
        try:
            session = Session.objects.get(key = session_key)
            messages.add(request, messages.SUCCESS,'You session has been started')
            request.session['session_key'] = session_key
        except:
            messages.add(request, messages.ERROR,'Your session doesn\'t exist')
    return response(request, redirect=reverse('main-home'))

def end(request):
    try:
        del request.session['session_key']
        messages.add(request,messages.SUCCESS,'Your session has been ended.')
    except:
        pass
    return response(request, redirect=reverse('main-home'))