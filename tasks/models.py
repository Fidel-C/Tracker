from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.






class TimeStamps(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        


User=get_user_model()



class Company(TimeStamps,models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    logo=models.ImageField(upload_to='companies',null=True,blank=True)
    is_active=models.BooleanField(default=False)
    creator=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Company'
        verbose_name_plural='Companies'
        ordering=['-updated_at']
        
   
            
        
    
class Employee(TimeStamps,models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company)


 
    def __str__(self):
        return f"{self.user.username}  | {self.user.first_name} | {self.user.last_name}"
    
   
    
    class Meta:
        ordering=['-created_at']
        
        
class Position(models.Model):
    title=models.CharField(max_length=300)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.employee.user.username} | {self.title} | {self.company.name}" 

    
        
        
    
    
    
    



    
    
    
class Task(TimeStamps,models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    started_at=models.DateTimeField()
    stopped_at=models.DateTimeField()
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee,models.CASCADE)
    

    def __str__(self):
        return self.title
    
    # def get_employee(self):
    #     return self.employee__user
    
    class Meta:
        ordering=['-updated_at']
    
    
    

    
    
    

