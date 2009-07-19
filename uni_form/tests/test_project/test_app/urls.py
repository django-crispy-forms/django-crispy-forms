from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^view_helper/$', "test_app.views.view_helper", name='view_helper'),    
    url(r'^form_helper/$', "test_app.views.form_helper", name='form_helper'),        
    
    )