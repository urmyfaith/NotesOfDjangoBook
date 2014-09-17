from django.shortcuts import render_to_response
from books.models import Book
from blog.models import blog
def blog_list(request):
    blog_list=blog.objects.all()
    return render_to_response('make_a_view_generic/blog_list.html',{'blogs':blog_list})
def book_list(request):
    book_list=Book.objects.all()
    return render_to_response('make_a_view_generic/book_list.html',{'books':book_list})

def object_list(request,model):
    obj_list=model.objects.all()
    key_name=model.__name__.lower()
    template_name='make_a_view_generic/%s_list.html' % key_name
    key_name=key_name+'s'
    return render_to_response(template_name,{key_name:obj_list})
