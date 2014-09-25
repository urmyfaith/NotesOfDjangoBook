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
                #return HttpResponse('You have logged in.')
                return HttpResponseRedirect('/chapter14/limited_acess_vote/')
            else:
                return HttpResponse('usrname or password invalid.')
    return render_to_response('user_login.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))
  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/chapter14/user/login/")


def vote_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("not authenticated.")
    else:
        return HttpResponse("yes authenticated.")

from django.contrib.auth.decorators import login_required
@login_required(login_url="/chapter14/user/login/")
#function under login_required, will be authenticate.
# if authentication failed,will return to login_url.
def poll_view(request):
    return HttpResponse("you are in poll_view")
    
    
