from django.urls import path
from . import views


urlpatterns = [
    path('new', views.new, name='new_gateway'),
]