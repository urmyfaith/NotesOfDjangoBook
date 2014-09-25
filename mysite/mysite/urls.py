from django.conf.urls import *
from django.contrib import admin
from books.models import Book
from blog.models import blog
from mysite import sendMailViewByForms
from mysite import articlesViews

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^books/', include('books.urls')),
)

##urlpatterns += patterns('mysite.sendMailViewByForms',
##    url(r'^contact/$','contact'),
##    url(r'^contact/thanks/$','contact_thanks'),                  
##)

urlpatterns += patterns('',
    url(r'^contact/$',sendMailViewByForms.method_splitter, \
        {'GET_method':sendMailViewByForms.get_contact, \
         'POST_method':sendMailViewByForms.post_contact}),
    url(r'^contact/thanks/$',sendMailViewByForms.contact_thanks),                  
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
    url(r'^chapter8_url_view/fake_captured_URLconf_values/articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$','day_archive'),
    url(r'^chapter8_url_view/fake_captured_URLconf_values/articles/birthday/$','day_archive',{'year':'2014','month':'09','day':'16'}),
)

urlpatterns += patterns('mysite.foobar_view',
    (r'^chapter8_url_view/pass_extra_options_to_view/foo/$', \
     'foo_bar_view',{'template_name':'foobar/foo.html','search_str':'world'}),
    (r'^chapter8_url_view/pass_extra_options_to_view/bar/$', \
     'foo_bar_view',{'template_name':'foobar/bar.html','search_str':'the'}),
)

urlpatterns += patterns('mysite.objectView',
    url(r'^chapter8_url_view/make_a_view_generic/blog/$','object_list',{'model':blog}),
    url(r'^chapter8_url_view/make_a_view_generic/book/$','object_list',{'model':Book}),
)

urlpatterns += patterns('mysite.blogPageView',
    url(r'^chapter8_url_view/use_default_view_arguments/blog/$','show_blog_page'),
    url(r'^chapter8_url_view/use_default_view_arguments/blog/page(?P<num>\d+)/$','show_blog_page'),
)

urlpatterns += patterns('',
    (r'^chapter8_requires_login/articles/(?P<year>\d{4})/$', articlesViews.year_archive),
    (r'^chapter8_requires_login/articles/(?P<year>\d{4})/(?P<month>\d{2})/$',articlesViews.month_archive),

)

from django.views.generic import TemplateView
urlpatterns += patterns('',
    url(r'^chapter11_generic_view/about/$', TemplateView.as_view(template_name="about.html")),
)


urlpatterns += patterns('mysite.show_non_html_content',
    url(r'^chapter13/show_images/(?P<filename>[\w-]+).png/$','show_images'),
    url(r'^chapter13/show_csv/$','show_csv'),
    url(r'^chapter13/show_csv2/$','show_csv2'),
    url(r'^chapter13/show_csv3/$','some_streaming_csv_view'),
    url(r'^chapter13/show_xls/$','show_xls'),
    url(r'^chapter13/show_pdf/$','show_pdf'),
    url(r'^chapter13/show_pdf_StringIO/$','show_pdf_StringIO'),
)


urlpatterns += patterns('mysite.cookie_view',
    url(r'^chapter14/show_color/$','show_color'),
    url(r'^chapter14/set_color/$','set_color'),
)

urlpatterns += patterns('mysite.session_view',
    url(r'^chapter14/post_comment/$','post_comment'),
    url(r'^chapter14/login/$','login'),
)
urlpatterns += patterns('mysite.user_login_logout_view',
    url(r'^chapter14/user/login/$','login'),
    url(r'^chapter14/user/logout/$','logout'),
    url(r'^chapter14/limited_acess_vote/$','vote_view'),
    url(r'^chapter14/limited_acess_poll/$','poll_view'),
    url(r'^chapter14/limited_acess_vote2/$','vote_view2'),
    url(r'^chapter14/user/register$','register'),
    url(r'^chapter14/user/user_data$','user_data_in_templates'), 
)

from django.contrib.auth.views import login,logout
urlpatterns += patterns('',
    url(r'^chapter14/accounts/login/$',login,{'extra_context': {'next': '/hello'}}),
    url(r'^chapter14/accounts/logout/$',logout),  
)

urlpatterns += patterns('mysite.user_message_view',
    url(r'^chapter14/message/playlist/(?P<songs>[\w-]+)/$','create_palylist'),
)
