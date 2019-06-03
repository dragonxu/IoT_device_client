from django.db import models
from datetime import date

# Create your models here.


class GatewayBase(models.Model):
    gateway_name = models.CharField(max_length=20, primary_key=True, null=False, verbose_name='网关名')
    description = models.TextField(max_length=200, default='', verbose_name='网关描述')
    sub_device = models.IntegerField(default=0, null=False)
    create_date = models.DateField(default=date.today, verbose_name='创建时间')


class MqttTopic(models.Model):
    topic = models.TextField(default='', verbose_name='Topic')
    function = models.CharField(max_length=10, null=False, verbose_name='功能')
    tag = models.CharField(max_length=20, null=True, default='', verbose_name='标签')
    description = models.TextField(max_length=200, default='')
