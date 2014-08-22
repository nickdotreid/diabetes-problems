from django.conf.urls import patterns, include, url

urlpatterns = patterns('ajax.views',
	url(r'^','home', name="ajax-home"),
)