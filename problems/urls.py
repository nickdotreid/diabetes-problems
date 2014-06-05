from django.conf.urls import patterns, include, url

urlpatterns = patterns('problems.views',
	url(r'^thanks','thanks'),
	url(r'^','important'),
)