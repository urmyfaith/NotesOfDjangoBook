# -*- coding: utf-8-*-
from django.http import HttpResponse,HttpResponseRedirect,Http404
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
                ['zuoxue@qq.com','904312072@qq.com'],
                )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        #GET Method ---default visite site method.
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_formByForms.html',{'form': form},context_instance=RequestContext(request))

def contact_thanks(request):
    return HttpResponse('<html><body><h1>thanks</h1></body></html>')

##def method_splitter(request,GET_method=None,POST_method=None):
##    if request.method =='POST' and POST_method is not None:
##        return POST_method(request)
##    elif request.method == 'GET' and  GET_method is not None:
##        return GET_method(request)
##    raise Http404

def method_splitter(request,*args,**kargs):
    get_method_view = kargs.pop('GET_method',None)
    post_method_view = kargs.pop('POST_method',None)
    if request.method == 'GET' and get_method_view is not None:
        return get_method_view(request,*args,**kargs)
    elif request.method =='POST' and post_method_view  is not None:
        return post_method_view(request,*args,**kargs)
    raise Http404

def get_contact(request):
    assert request.method == 'GET'
    form = ContactForm(initial={'subject': 'amazing site!'})
    return render_to_response('contact_formByForms.html',{'form': form},context_instance=RequestContext(request))
def post_contact(request):
    assert request.method == 'POST'
    form = ContactForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        send_mail(
            cd['subject'],
            cd['message'],
            cd.get('email','urmyfaith@qq.com'),
            ['1278908611@qq.com','urmyfaith@qq.com'],         
            )
        print 'send_mail_sucess'
        return HttpResponseRedirect('/contact/thanks/')
    return HttpResponseRedirect('/contact/')
