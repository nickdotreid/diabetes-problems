from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

def page(request):
	# check session and switch initial content?
	return render_to_response('ajax.html',{
        },context_instance=RequestContext(request))