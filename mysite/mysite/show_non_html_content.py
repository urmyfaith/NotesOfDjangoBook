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

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

from django.utils.six.moves import range
from django.http import StreamingHttpResponse
def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {0}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response

import xlwt
from datetime import datetime
def show_xls(request):
    response=HttpResponse(content_type='text/xls')
    response['Content-Disposition'] = 'attachment; filename="show_xls.xls"'
    
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
            num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    ws.write(0, 0, 1234.56, style0)     #num
    ws.write(1, 0, datetime.now(), style1)  #time
    ws.write(2, 0, 1)
    ws.write(2, 1, 1)
    ws.write(2, 2, xlwt.Formula("$A3+$B3"))   #Formula
    
    wb.save(response)
    
    return response


from reportlab.pdfgen import canvas    
def show_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="show_pdf.pdf"'

    #create PDF
    p = canvas.Canvas(response)
    p.drawString(300,500,"output PDF in Django by reportlab")
    p.showPage()
    p.save()
    return response

from cStringIO import StringIO
def show_pdf_StringIO(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="show_pdf_StringIO.pdf"'

    temp=StringIO()
    print type(temp)

    p=canvas.Canvas(temp)
    p.drawString(250,500,"create pdf by reportelab,StringIO()")
    p.showPage()
    p.save()
    response.write(temp.getvalue())
    return response

