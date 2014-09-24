# -*- coding: utf-8-*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib import auth

def login(request):
    errors=[]
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not request.POST.get('username',''):
            errors.append('Enter a username.')
        if not request.POST.get('password',''):
            errors.append('Enter a password.')
        if not errors:
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponse('You have logged in.')
            else:
                return HttpResponse('usrname or password invalid.')
    return render_to_response('user_login.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))
  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/chapter14/user/login/")
