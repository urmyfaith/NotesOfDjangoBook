# -*- coding: utf-8-*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def post_comment(request):
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('subject',''):
            errors.append('Enter a subject.')
        if not request.POST.get('message',''):
            errors.append('Enter a meeage.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if request.session.get('has_commented', False):
           return HttpResponse("You've already commented.")
        if not errors:
            #do something here, eg: save it to database
            request.session['has_commented'] = True
            return HttpResponse('Thanks for your comment!')
    return render_to_response('post_comment.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))

def login(request):
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('username',''):
            errors.append('Enter a username.')
        if not request.POST.get('password',''):
            errors.append('Enter a password.')
        if not errors:
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                return HttpResponse("Logged in.")
            else:
                return HttpResponse('Please enable coookie.')
    request.session.set_test_cookie()
    return render_to_response('login.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))
  
