from django.db import models

# Create your models here.


class GatewayBase(models.Model):
    gateway_id = models.CharField(max_length=20, verbose_name='网关id')
    description = models.CharField(max_length=200, verbose_name='网关描述')
