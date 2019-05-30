from django.db import models

# Create your models here.


class GatewayBase(models.Model):
    gateway_name = models.CharField(max_length=20, verbose_name='网关名')
    description = models.CharField(max_length=200, verbose_name='网关描述')
    sub_device = models.IntegerField(default=0)
    create_date = models.DateField(verbose_name='创建时间')

