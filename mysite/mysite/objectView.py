from django.shortcuts import render_to_response
from books.models import Book
from blog.models import blog
def blog_list(request):
    blog_list=blog.objects.all()
    return render_to_response('make_a_view_generic/blog_list.html',{'blogs':blog_list})
def book_list(request):
    book_list=Book.objects.all()
    return render_to_response('make_a_view_generic/book_list.html',{'books':book_list})


