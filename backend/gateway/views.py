from django.shortcuts import render
from django.http import HttpResponse
from .models import GatewayBase
import json


def new(request):
    gateway_id = request.POST['gateway_id']
    description = request.POST['description']
    gateway = GatewayBase()
    gateway.gateway_id = gateway_id
    gateway.description = description
    gateway.save()

    return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')

