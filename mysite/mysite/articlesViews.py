# -*- coding: utf-8-*-
from django.http import HttpResponse

def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,month,year):
    rawHtml='<html><head></head><body>month_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
def day_archive(request,month,year,day):
    rawHtml='<html><head></head><body>day_archive:%s-%s-%s</body></html>'% (year,month,day)
    return HttpResponse(rawHtml)
