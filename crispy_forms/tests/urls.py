from django.http import HttpResponse


try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url



def simpleAction(request):
    return HttpResponse()


urlpatterns = patterns('',
    url(r'^simple/action/$', simpleAction, name = 'simpleAction'),
)
