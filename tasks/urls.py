from django.urls import path
from tasks import views




urlpatterns = [
    path('',views.index,name='index'),
    path('tasks/create/<int:position_id>/',views.create_entry,name='create_tasks'),
    path('tasks/update/<int:task_id>/',views.update_task,name='update_tasks'),
    path('tasks/delete/<int:task_id>/',views.delete_task,name='delete_tasks'),
    path('companies/create/',views.register_org,name='create_company'),
    path('companies/<int:company_id>/',views.company_details,name='company_details'),

]


