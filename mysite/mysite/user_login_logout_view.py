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
    
    
def user_can_vote(user):
    #return user.is_authenticated() and user.has_perm("poll.can_vote")
    return user.is_authenticated()
from django.contrib.auth.decorators import user_passes_test
@user_passes_test(user_can_vote,login_url="/chapter14/user/login/")
def vote_view2(request):
    return HttpResponse("vote_view2 under user_passes_test.")

from django import forms
from django.contrib.auth.forms import UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/chapter14/user/login/')
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", \
                              {'form':form}, \
                              context_instance=RequestContext(request))

def user_data_in_templates(request):
    return render_to_response("use_data_in_templates.html",context_instance=RequestContext(request))
    
    
