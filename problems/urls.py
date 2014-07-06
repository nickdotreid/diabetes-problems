from django.conf.urls import patterns, include, url

urlpatterns = patterns('problems.views',
	url(r'^problems','important'),
	url(r'^add','add'),
	url(r'^survey','survey'),
	url(r'^email','email'),
	url(r'^','thanks'),
)