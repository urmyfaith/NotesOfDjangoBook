# -*- coding: utf-8-*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.template import RequestContext
import datetime
from mysite.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email','urmyfaith@qq.com'),
                ['1278908611@qq.com','904312072@qq.com'],
                )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        #GET Method ---default visite site method.
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_formByForms.html',{'form': form},context_instance=RequestContext(request))
def contact_thanks(request):
    return HttpResponse('<html><body><h1>thanks</h1></body></html>')
