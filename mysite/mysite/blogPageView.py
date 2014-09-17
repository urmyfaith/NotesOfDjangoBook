from django.http import HttpResponse

def show_blog_page(request,num='1'):
    rawHtml='<html><head></head><body>you are at page:%s.</body></html>'% num
    return HttpResponse(rawHtml)

