from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('create_tcp', views.create_tcp),
    path('getAll', views.get_all),
    path('delate', views.delate)
]
