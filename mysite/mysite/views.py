from django.http import Http404,HttpResponse
import datetime
from django.shortcuts import render_to_response

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
    request_path = request.path
    request_host = request.get_host()
    request_full_path = request.get_full_path()
    request_is_secure = request.is_secure()
    request_dic={
        'request_path':request_path,
        'request_host':request_host,
        'request_full_path':request_full_path,
        'request_is_secure':request_is_secure,
        }
    request_meat_values = request.META.items()
    request_meat_values.sort()
    return render_to_response('show_request.html',{
        'request_dic':request_dic,
        'request_meat_values':request_meat_values,
        })
