from django.shortcuts import get_object_or_404

from django.views.generic import ListView,DetailView
from books.models import Publisher,Book,Author
from django.utils import timezone

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
    
class AuthorDetailView(DetailView):
    queryset=Author.objects.all()
    def get_object(self):      
        mobject = super(AuthorDetailView,self).get_object()
        mobject.last_accessed=timezone.now()
        mobject.save() 
        return mobject
    
    def get_context_data(self,*args,**kwargs):
        context=super(AuthorDetailView,self).get_context_data(*args,**kwargs)
        mm_object=get_object_or_404(Author,id=self.kwargs['pk'])
        m_object = super(AuthorDetailView,self).get_object()
        context['author']=m_object
        print context
        return context
