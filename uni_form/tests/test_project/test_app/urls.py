from django.conf.urls.defaults import *



urlpatterns = patterns('',

    url(r'^view_helper/$', "test_app.views.view_helper", name='view_helper'),    
    url(r'^form_helper/$', "test_app.views.form_helper", name='form_helper'),        
    url(r'^layout_test/$', "test_app.views.layout_test", name='layout_test'),            
    url(r'^view_helper_set_action/$', "test_app.views.view_helper_set_action", name='set_action_test'),     
    
    
    )