from django.conf.urls import patterns, include, url

urlpatterns = patterns('problems.views',
	url(r'^(?P<session_key>\w+)/problems','important'),
	url(r'^(?P<session_key>\w+)/email','email'),
	url(r'^(?P<session_key>\w+)','thanks'),
	url(r'^','important'),
)