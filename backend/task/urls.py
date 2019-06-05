from django.urls import path
from . import views

urlpatterns = [
    path('getAll', views.get_all),
    path('delete', views.delete),
    path('create', views.create),
    path('edit', views.edit),
    path('addRecord', views.add_record)
]
