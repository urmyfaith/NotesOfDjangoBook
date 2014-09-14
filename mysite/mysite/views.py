# -*- coding: utf-8-*-
from django.http import Http404,HttpResponse,HttpResponseRedirect
import datetime
from django.shortcuts import render_to_response
from books.models import Book
from django.core.mail import send_mail
from django.template import RequestContext

def hello(request):
    return HttpResponse("Hello zx.")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('date/current_datetime.html',{'current_date':now})
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    # return HttpResponse(html)
    return render_to_response('date/future_datetime.html',{
                                                           'hour_offset':offset,
                                                           'next_time':dt
                                                           })
def show_request(request):
    request_dic={
        'request_path': request.path,
        'request_host': request.get_host(),
        'request_full_path':request.get_full_path(),
        'request_is_secure':request.is_secure(),
        }
    request_meat_values = request.META.items()
    request_meat_values.sort()
    return render_to_response('show_request.html',{
        'request_dic':request_dic,
        'request_meat_values':request_meat_values,
        })
def search_form(request):
    return render_to_response('search_form.html',)

def show_search_result(request):
    if 'q' in request.GET:
        #message = 'You searched for : %r' % request.GET['q']
        #message = 'You searched for : %s' % request.GET['q']
        search_str = request.GET['q']
        if search_str!="":
            books = Book.objects.filter(title__icontains=search_str)
            return render_to_response('search_results.html',{
            'books':books,
            'search_str':search_str
            })
        #message = 'You submitted an empty form.'
        #return HttpResponse(message)
        return render_to_response('search_form.html', {'error': True})

