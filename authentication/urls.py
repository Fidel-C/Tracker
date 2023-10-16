from django.urls import path
from authentication import views





urlpatterns=[
   path('register/',views.signup,name='signup'), 
   path('login/',views.login_view,name='login'), 
   path('profile/',views.profile,name='profile'),
    
]




