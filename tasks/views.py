from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.
from django import forms
from django.urls import reverse
from .models import Employee, Position, Task,Company
from .forms import CompanyDetailsForm, CompanyForm, TaskForm, UpdateTask
from django.http import HttpResponseBadRequest


def index(request):
    return render(request,'tasks/index.html',{})



@login_required(login_url='/auth/login')
def create_entry(request,position_id):
    form = TaskForm(position_id=position_id,user=request.user, data=request.POST)
    if request.method=='POST':
       if form.is_valid():
           form.save()
           messages.success(request,'Entry Added Successfully')
           return redirect('profile')
           
       return render(request,'tasks/create_tasks.html',{'form':form})
  
    return render(request,'tasks/create_tasks.html',{'form':form})
        
        
@login_required(login_url='/auth/login')        
def update_task(request,task_id):
    task=get_object_or_404(Task,id=task_id)
    if request.method=='POST':
        form=UpdateTask(data=request.POST,instance=task)
        if form.is_valid():
            form.save()
            messages.success(request,'Task Updated Successfully')
            return redirect('profile')
            
        else:
            return render(request,'tasks/update_tasks.html',form)
    else:
        form=UpdateTask(instance=task)
        context={'form':form}
        return render(request, 'tasks/update_tasks.html',context)
    
    
@login_required(login_url='/auth/login')    
def delete_task(request, task_id):
    task=get_object_or_404(Task,id=task_id)
    task.delete()
    messages.success(request,'Task Deleted Successfully')
    return redirect('profile')
        
        
        
        
        
        
@login_required(login_url='/auth/login')
def register_org(request):
    if request.method=="POST":
        form= CompanyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request,'Organisation created successfully')
            return redirect('profile')
        else:
            return render(request,'org/register.html',{'form':form})
    else:
        form=CompanyForm()
        orgs=request.user.company_set.all()
        return render(request,'org/register.html',{'form':form,'orgs':orgs})
    
    
    
    
    
    
@login_required(login_url='/auth/login')
def company_details(request,company_id):
    company=get_object_or_404(Company,id=company_id)
    staff=Position.objects.filter(company__creator=request.user)
    tasks=Task.objects.filter(company__creator=request.user)
    if company.creator==request.user:
        if request.method=="POST":
            form=CompanyDetailsForm(data=request.POST or None)    
            if form.is_valid():
                try:
                    existing=Employee.objects.get(user__email=form.cleaned_data['email'])
                    if form.cleaned_data['action']=='add' and form.cleaned_data['position'] !='':   
                        exists=Position.objects.filter(employee=existing).filter(company=company).first()
                        if not exists:
                            company.employee_set.add(existing)
                            Position.objects.create(employee=existing,company=company,title=form.cleaned_data['position'])
                            messages.success(request,'Successfully added')
                            context={"form":form,'staff':staff}
                            company.save()   
                            return render(request,'org/company_details.html',context)                                                                                     
                        else:
                            messages.error(request,'This user is already your staff')
                            context={"form":form,'staff':staff}          
                            return render(request,'org/company_details.html',context)                                      
                    elif form.cleaned_data['action']=='remove':
                        exists=Position.objects.filter(company=company).filter(employee=existing)
                        if exists:
                            company.employee_set.remove(existing) 
                            exists.delete()
                            messages.success(request,'Successfully removed')
                            company.save()
                            context={"form":form,'staff':staff}
                            return render(request,'org/company_details.html',context)
                        else:
                           messages.error(request,'You don\'t have a staff with that email')
                           context={"form":form,'tasks':tasks,'staff':staff}
                           return render(request,'org/company_details.html',context)
                except Employee.DoesNotExist:
                    messages.error(request,'Email not found')
                    context={"form":form,'staff':staff}
                    return render(request,'org/company_details.html',context)           
            context={"form":form,'tasks':tasks,'staff':staff}
            return render(request,'org/company_details.html',context)
        else:   
            form=CompanyDetailsForm()
            context={"form":form,'tasks':tasks,'staff':staff}
            return render(request,'org/company_details.html',context)
    else:
        return HttpResponseBadRequest({})
        
       
    
    
    
        