from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^simple/action/$', 'simpleAction', name = 'simpleAction'),
)
