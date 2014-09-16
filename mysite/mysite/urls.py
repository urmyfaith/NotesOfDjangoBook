from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/$','mysite.sendMailViewByForms.contact'),
    url(r'^contact/thanks/$','mysite.sendMailViewByFormscontact_thanks'),                  
)
urlpatterns += patterns('mysite.views',
    url(r'^hello/$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    url(r'^search/$','show_search_result'),
    url(r'^request-info/$','show_request'),
    url(r'^search-form/$','search_form'),
)
