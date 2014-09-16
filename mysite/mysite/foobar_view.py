from django.shortcuts import render
from books.models import Book
def foo_view(request):
    books = Book.objects.filter(title__icontains='world')  
    return render(request,'foobar/foo.html',{'books':books})
def bar_view(request):
    books = Book.objects.filter(title__icontains='the')
    return render(request,'foobar/bar.html',{'books':books})
