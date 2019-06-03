from django.urls import path
from . import views


urlpatterns = [
    path('new', views.new, name='new_gateway'),
    path('delate', views.delate, name='删除网关'),
    path('getAll', views.get_all),
    path('mqtt_config', views.mqtt_config),
    path('createTopic', views.create_topic),
    path('getAllTopic', views.get_all_topic),
    path('delTopic', views.del_topic),
    path('editTopic', views.edit_topic)
]