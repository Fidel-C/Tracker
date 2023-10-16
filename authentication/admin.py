from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.






class UserAdmin(admin.ModelAdmin):
    list_display=['email','username','phone','is_active','is_staff','is_superuser','date_joined','last_login']
    search_fields=['email','username','phone']

admin.site.register(get_user_model(),UserAdmin)



    