from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

import json

from problems.models import Session

def response(request, data={}, template="base.html", error=False, redirect=False):
    if request.is_ajax():
    	if template:
    		content = render_to_string(template, data, context_instance=RequestContext(request))
    		data = {'content', content}
    	# append any messages & clear message buffer
    	return HttpResponse(
    		json.dumps(data),
    		mimetype='application/json',
    		)
    if redirect:
    	return HttpResponseRedirect(redirect)
    return render_to_response(
    	template,
    	data,
    	context_instance=RequestContext(request)
    	)	

def home(request):
	return response(request,
		template="home.html")

def thanks(request):
    if 'session_key' not in request.session:
        return home(request)
    session, created = Session.objects.get_or_create(key=request.session['session_key'])
    
    survey_form = SurveyForm(session=session)
    email_form = EmailForm(session=session)

    return response(request,
    	data = {
        'form':survey_form,
        'email_form':email_form,
        },
        template='problems/thanks.html',
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