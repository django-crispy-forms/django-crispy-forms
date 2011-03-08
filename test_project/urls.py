from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', "test_app.views.basic_test", name='test_index'),
    (r'^more/', include('test_app.urls')),

    (r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
