from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^test$', "views.test_me", name='wiki_index'),
    
    )