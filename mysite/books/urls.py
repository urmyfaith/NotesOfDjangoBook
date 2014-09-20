from django.conf.urls import *
from books.views import PublisherList

urlpatterns = patterns('books.views',
    url(r'^publishers/$',PublisherList.as_view()),
)
