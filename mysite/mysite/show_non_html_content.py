# -*- coding: utf-8 -*-
from django.http import HttpResponse
import csv

def show_images(request,filename):
    image_data=open("D:\\Documents\\GitHub\\NotesOfDjangoBook\\notes\\images\\%s.png" % filename,"rb")
    return HttpResponse(image_data,content_type="image/png")

def show_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="show_csv.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row',"hello"])
    writer.writerow(['Second row', 'A',"Here's a quote"])

    return response

UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,281,304,203]
def show_csv2(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=show_csv.csv'
    writer = csv.writer(response)
    writer.writerow(['Year', 'Unruly Airline Passengers'])
   #for (year, num) in zip(range(1995, 2006), UNRULY_PASSENGERS):
        #writer.writerow([year, num])
        #print [year,num]
    for row in zip(range(1995, 2006), UNRULY_PASSENGERS):
        #(1995,146)==>[1995,146]
       writer.writerow(list(row))
    return response
