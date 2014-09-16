from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('mysite.sendMailViewByForms',
    url(r'^contact/$','contact'),
    url(r'^contact/thanks/$','contact_thanks'),                  
)
urlpatterns += patterns('mysite.views',
    url(r'^hello/$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    url(r'^search/$','show_search_result'),
    url(r'^request-info/$','show_request'),
    url(r'^search-form/$','search_form'),
)

urlpatterns += patterns('mysite.articlesViews',
    (r'^chapter8_url_view/name_groups/articles/(?P<year>\d{4})/$', 'year_archive'),
    (r'^chapter8_url_view/name_groups/articles/(?P<year>\d{4})/(?P<month>\d{2})/$','month_archive'),
)

urlpatterns += patterns('mysite.foobar_view',
    (r'^chapter8_url_view/pass_extra_options_to_view/foo/$','foo_view'),
    (r'^chapter8_url_view/pass_extra_options_to_view/bar/$','bar_view'),
)
