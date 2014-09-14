from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.views import hello,current_datetime,hours_ahead,show_request,search_form,show_search_result

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$',hello),
    url(r'^time/$',current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^request-info/$',show_request),
    url(r'^search-form/$',search_form),
    url(r'search/$',show_search_result),
)
