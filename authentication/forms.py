from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms







class CreateUserForm(UserCreationForm):
    class Meta:
       fields=['first_name','last_name','username','phone','email']
       model=get_user_model()
       
 
    