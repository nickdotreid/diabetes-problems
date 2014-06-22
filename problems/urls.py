from django.conf.urls import patterns, include, url

urlpatterns = patterns('problems.views',
	url(r'^(?P<session_key>\w+)/thanks','thanks'),
	url(r'^(?P<session_key>\w+)','important'),
	url(r'^','important'),
)