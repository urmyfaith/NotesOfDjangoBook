from django.conf.urls import *
from books.views import PublisherBookList

urlpatterns = patterns('books.views',
    url(r'^publishers/([\w-]+)/$',PublisherBookList.as_view()),
)
