from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

def important(request):
    return render_to_response('problems/important.html',{
        'problems':[],
        },context_instance=RequestContext(request))