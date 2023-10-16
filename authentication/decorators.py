from django.shortcuts import redirect,HttpResponseRedirect,resolve_url






def guest_guard(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(resolve_url('profile'))
        else:
            return func(request,*args,**kwargs)
    return wrapper
    