import django

if django.get_version() >= '1.5':
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse


def simpleAction(request):
    return HttpResponse()


urlpatterns = patterns('',
    url(r'^simple/action/$', 'crispy_forms.tests.urls.simpleAction', name = 'simpleAction'),
)


