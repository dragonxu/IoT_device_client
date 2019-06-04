
from django.db import models
from gateway.models import GatewayBase
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=20, null=False)
    gateway = models.ForeignKey(GatewayBase, on_delete=models.CASCADE, to_field='gateway_name')
    description = models.TextField(default='', max_length=200)
    protocol = models.CharField(default='modbus', max_length=10)
    create_time = models.DateField()
    status = models.BooleanField(default=False)