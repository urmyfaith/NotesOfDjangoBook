from django.conf.urls import *
from django.contrib import admin
#from mysite.views import hello,current_datetime,hours_ahead,show_request,search_form,show_search_result
from mysite import views
#from mysite.sendMailView import contact,contact_thanks

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^hello/$',hello),
    url(r'^hello/$',views.hello),
    #url(r'^time/$',current_datetime),
    url(r'^time/$',views.current_datetime),
    #url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead), 
    #url(r'^request-info/$',show_request),
    url(r'^request-info/$',views.show_request),
    #url(r'^search-form/$',search_form),
    url(r'^search-form/$',views.search_form),
    #url(r'^search/$',show_search_result),
    url(r'^search/$',views.show_search_result),
    url(r'^contact/$','mysite.sendMailViewByForms.contact'),
    url(r'^contact/thanks/$','mysite.sendMailViewByFormscontact_thanks'),                  
)
