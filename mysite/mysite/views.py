from django.http import Http404
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
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
    
