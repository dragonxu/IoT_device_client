from django.urls import path
from . import views

urlpatterns = [
    path('getAll', views.get_all),
    path('delete', views.delete),
    path('create', views.create),
    path('edit', views.edit),
    path('addRecord', views.add_record),
    path('getAllRecord', views.get_all_record),
    path('deleteRecord', views.delete_record),
    path('changeStatus', views.change_status),
    path('startTask', views.start_task)
]
