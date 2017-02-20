from django.conf.urls import url
from django.views.generic import View

urlpatterns = [
    url(r'^simple/action/$', View.as_view(), name='simpleAction'),
]
