from django.db import models
from gateway.models import GatewayBase
# Create your models here.


class TCP_device(models.Model):
    device_name = models.CharField(max_length=20, null=False)
    slave_id = models.IntegerField(null=False)
    description = models.TextField(max_length=200, default='', verbose_name='设备描述')
    create_time = models.DateField(null=False)
    protocol_way = models.CharField(max_length=3, null=False, verbose_name='设备接入方式')
    last_active = models.DateField(auto_now=True)
    gateway_name = models.ForeignKey(GatewayBase, on_delete=models.CASCADE, to_field='gateway_name')
