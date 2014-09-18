
def requires_login(view):
    def logined_view(request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request,*args,**kwargs)
    return loginde_view
