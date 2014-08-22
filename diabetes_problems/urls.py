from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views import generic

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns("",
    # Admin URLs.
    url(r"^admin/", include(admin.site.urls)),
    # There's no favicon here!
    url(r"^favicon.ico$", generic.RedirectView.as_view()),
    url(r"^issues/", include('problems.urls')),
    url(r"^", include('main.urls')),
)

if settings.MEDIA_SERVE:
	urlpatterns = patterns("",
		 (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
		) + urlpatterns