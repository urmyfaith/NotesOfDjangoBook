# -*- coding: utf-8-*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.template import RequestContext
import datetime

def contact(request):
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('subject',''):
            errors.append('Enter a subject.')
        if not request.POST.get('message',''):
            errors.append('Enter a meeage.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email','urmyfaith@qq.com'),
                ['1278908611@qq.com','904312072@qq.com'],
                #html_message=html_message_head+html_message_end
                #html_message=html_message_head+send_time+html_message_end
                #html_message="<html><body>It's time : %s </body></html>" % datetime.datetime.now()
                )
            return HttpResponseRedirect('/contact/thanks/')
    return render_to_response('contact_form.html',{'errors':errors,},context_instance=RequestContext(request))
def contact_thanks(request):
    return HttpResponse('<html><body><h1>thanks</h1></body></html>')
