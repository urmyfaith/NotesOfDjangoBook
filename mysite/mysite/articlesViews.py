# -*- coding: utf-8-*-
from django.http import HttpResponse

def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,year,month):
    rawHtml='<html><head></head><body>year_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
