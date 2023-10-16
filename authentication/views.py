from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,resolve_url,redirect
from authentication.forms import CreateUserForm
from django.contrib import messages
# Create your views here.
from authentication.decorators import guest_guard
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from tasks.models import Company, Employee, Position


@guest_guard
def signup(request):
    if request.method=='POST':
        form=CreateUserForm(data=request.POST)        
        if form.is_valid():
            form.save()
            messages.success(request,message='Account Created Successfully')
            return redirect('profile')
        else:
            context={'form':form}
            return render(request,'registration/signup.html',context)             
    else:
        context={'form':CreateUserForm()}
        return render(request,'registration/signup.html',context)
    
    
@guest_guard
def login_view(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('profile')
        else:
            return render(request,'registration/login.html',{'form':form})
    return render(request,'registration/login.html',{'form':AuthenticationForm(request)})
          
    
    
    
@login_required(login_url='/auth/login')
def profile(request):
    if request.method=='GET':
        tasks=request.user.employee.task_set.all()
        jobs=Position.objects.filter(employee__user=request.user)
        return render(request,'tasks/profile.html',{'jobs':jobs,'tasks':tasks})
    