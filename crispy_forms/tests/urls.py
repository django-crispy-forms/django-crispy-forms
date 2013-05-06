import django

if django.get_version() >= '1.5':
    from django.conf.urls import *
else:
    from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^simple/action/$', 'simpleAction', name = 'simpleAction'),
)
