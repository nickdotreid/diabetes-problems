from django.conf.urls import patterns, include, url

urlpatterns = patterns('main.views',
	url(r'^email','email', name="main-email"),
	url(r'^survey','survey', name="main-survey"),
	url(r'^end','end', name="session-end"),
	url(r'^start(?P<session_key>\w+)','start', name="session-start"),
	url(r'^','home', name="main-home"),
)