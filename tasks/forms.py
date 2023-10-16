from django import forms


from .models import Employee, Position,Task,Company
from django.contrib.auth import get_user_model



class UpdateTask(forms.ModelForm):
     class Meta:
         model=Task
         exclude=['company','employee']
         widgets={
             'started_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
             'stopped_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
                  
                  }
         


class CompanyForm(forms.ModelForm):
    class Meta:
        exclude=['is_active','creator']
        model=Company
        
        
    def save(self,commit=True,user=None):
        instance=super().save(commit=False)
        if user:
            instance.creator=user
        if commit:
            instance.save()
        return instance
         
        
         
class CompanyDetailsForm(forms.Form):
    email=forms.EmailField(required=True,help_text='The email address of the user you want to add or remove from your organisation')
    position=forms.CharField(required=False,help_text='This is the position the user will hold in your organisation. eg Manager, Legal Officer, Intern,etc')
    action=forms.ChoiceField(choices=[('add','ADD'),('remove','REMOVE')],required=True)
    
    
        

    
    

class TaskForm(forms.ModelForm):
    position=forms.ChoiceField()
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'started_at','stopped_at','employee','company' ]
        widgets={'started_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
                 'stopped_at':forms.DateTimeInput(attrs={'type':'datetime-local'})}
        
        


    def __init__(self, position_id,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        current_pos=Position.objects.get(id=position_id)

        # Limit the choices for 'company' field to companies associated with the user
        self.fields['position'].choices=[(position.id,position.title) for position in Position.objects.filter(id=position_id) ]
        self.fields['company'].choices = [(co.company.id,co.company.name) for co in Position.objects.filter(id=current_pos.id)]
        self.fields['employee'].queryset = Employee.objects.filter(user=user)
        
     
        
    
        
        
       
