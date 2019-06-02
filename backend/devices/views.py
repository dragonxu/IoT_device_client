from django.shortcuts import render
from django.http import HttpResponse
import json
from django.utils import timezone
from .models import TCP_device
from gateway.models import GatewayBase


# Create your views here.


def test(request):
    return HttpResponse(json.dumps({'name': 'aaa'}), content_type='application/json')


def create_tcp(request):
    device = TCP_device()
    try:
        device.device_name = request.POST['name']
        device.description = request.POST['description']
        device.ip = request.POST['ip']
        device.port = request.POST['port']
        device.slave_id = request.POST['slave']
        device.gateway_name = GatewayBase.objects.get(gateway_name=request.POST['gateway_name'])
        device.create_time = timezone.datetime.now()
        device.protocol_way = 'TCP'
        device.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(str(e))
        return HttpResponse(json.dumps({'msg': '创建失败：' + str(e)}), content_type='application/json')


def get_all(request):
    gateway_name = request.POST.get('gateway_name')
    result = []
    if gateway_name:
        all_tcp = TCP_device.objects.filter(gateway_name=gateway_name)
        # RTU
    else:
        all_tcp = TCP_device.objects.all()
        # RTU
    for i in all_tcp:
        result.append({
            'name': i.device_name,
            'slave': i.slave_id,
            'description': i.description,
            'protocal': i.protocol_way,
            'create_time': i.create_time.strftime('%Y-%m-%d'),
            'gateway_name': i.gateway_name.gateway_name
        })
    return HttpResponse(json.dumps({'msg': 'ok', 'data': result}), content_type='application/json')


def delate(request):
    try:
        device = json.loads(request.POST['device'])
        print('网关：', device)
        for i in device:
            TCP_device.objects.filter(device_name=i['name'], gateway_name=i['gateway']).delete()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(str(e))
        return HttpResponse(json.dumps({'msg': '删除失败：' + str(e)}), content_type='application/json')
