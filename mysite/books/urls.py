from django.conf.urls import *
from books.views import PublisherBookList,AuthorDetailView

urlpatterns = patterns('books.views',
    url(r'^publishers/([\w-]+)/$',PublisherBookList.as_view()),
    url(r'^authors/(?P<pk>\d+)/$',AuthorDetailView.as_view()),
)
