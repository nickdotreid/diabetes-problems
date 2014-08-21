from django.conf.urls import patterns, include, url

urlpatterns = patterns('problems.views',
	url(r'^suggestion','suggestion', name="suggestion-add"),
	url(r'^order','order', name="problems-order"),
	url(r'^problems','pick', name="problems-pick"),
	url(r'^survey','survey'),
	url(r'^email','email'),
	url(r'^end','end'),
	url(r'^start/(?P<session_key>\w+)','start'),
	url(r'^','thanks'),
)