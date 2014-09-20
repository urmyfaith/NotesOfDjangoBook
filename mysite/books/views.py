from django.shortcuts import get_object_or_404

from django.views.generic import ListView
from books.models import Publisher,Book

class PublisherBookList(ListView):
    template_name="books/books_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher,name=self.args[0])
        return Book.objects.filter(publisher=self.publisher)
    def get_context_data(self,**kwargs):
        print "self.args[0]=",self.args[0]
        context=super(PublisherBookList,self).get_context_data(**kwargs)
        context['publisher']=self.publisher
        return context
    
    

