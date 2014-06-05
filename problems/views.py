from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

from problems.models import Problem, Session, Important

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
    return render_to_response('problems/important.html',{
        'problems':Problem.objects.all(),
        },context_instance=RequestContext(request))

def thanks(request):
    return render_to_response('problems/thanks.html',{},context_instance=RequestContext(request))