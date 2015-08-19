from django.conf.urls import patterns, url
from django.views.generic import View


urlpatterns = patterns(
    '',
    url(r'^simple/action/$', View.as_view(), name='simpleAction'),
)
