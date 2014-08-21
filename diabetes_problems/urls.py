from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views import generic

from django.template import add_to_builtins
add_to_builtins('athumb.templatetags.thumbnail')

admin.autodiscover()

urlpatterns = patterns("",

    # Admin URLs.
    url(r"^admin/", include(admin.site.urls)),
    # There's no favicon here!
    url(r"^favicon.ico$", generic.RedirectView.as_view()),
    url(r"^$", 'ajax.views.page'),
    url(r"^", include('problems.urls')),
)
