from django.urls import path
from . import views


urlpatterns = [
    path('new', views.new, name='new_gateway'),
    path('delate', views.delate, name='删除网关'),
    path('getAll', views.get_all)
]