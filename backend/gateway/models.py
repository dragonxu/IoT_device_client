from django.db import models
from datetime import date

# Create your models here.


class GatewayBase(models.Model):
    gateway_name = models.CharField(max_length=20, null=False, verbose_name='网关名')
    description = models.TextField(max_length=200, default='', verbose_name='网关描述')
    sub_device = models.IntegerField(default=0, null=False)
    create_date = models.DateField(default=date.today, verbose_name='创建时间')

