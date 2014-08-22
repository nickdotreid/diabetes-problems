from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

from main.views import home as main_home

def home(request):
	if not request.is_ajax():
		del request.session['session_key']
	return main_home(request)