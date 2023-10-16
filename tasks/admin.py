from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model


from tasks.models import (Employee,Company, Position,Task)


class PositionInline(admin.TabularInline):
    model=Position




class TaskInline(admin.TabularInline):
    model=Task
    readonly_fields=['title','description','employee','company','started_at','stopped_at']
    extra=1


class EmployeeInline(admin.TabularInline):
    model=Employee.companies.through
    extra=1
    





class CompanyInline(admin.TabularInline):
    model=Employee.companies.through
    
        
        


class EmployeeAdmin(admin.ModelAdmin):
    list_display=['user',]
    inlines=[TaskInline,PositionInline]
    class Meta:
        model=Employee



class CompanyAdmin(admin.ModelAdmin):
    search_fields=['name']
    list_display=['name','logo','created_at','updated_at']
    inlines=[TaskInline,EmployeeInline]
    class Meta:
        model=Company
        
        
        

        

admin.site.register(Company,CompanyAdmin)



admin.site.register(Employee,EmployeeAdmin)

admin.site.register(Task)
admin.site.register(Position)