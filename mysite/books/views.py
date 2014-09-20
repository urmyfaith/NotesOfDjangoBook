from django.shortcuts import render

from django.views.generic import ListView
from books.models import Publisher

class PublisherList(ListView):
    model = Publisher
