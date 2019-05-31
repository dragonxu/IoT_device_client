import json
from django.http import HttpResponse
from .models import GatewayBase
from django.utils import timezone


def new(request):
    try:
        gateway_name = request.POST['gateway_name']
        description = request.POST['description']
        gateway = GatewayBase()
        gateway.gateway_name = gateway_name
        gateway.description = description
        gateway.create_date = timezone.datetime.now()
        gateway.sub_device = 0
        gateway.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '创建失败'}), content_type='application/json')


def delate(request):
    try:
        gateway_name = request.POST['name']
        print(gateway_name)
        for name in gateway_name.split(','):
            GatewayBase.objects.get(gateway_name=name).delete()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '删除失败'}), content_type='application/json')


def get_all(request):
    all_gateway = GatewayBase.objects.all()
    result = []
    for i in all_gateway:
        result.append(
            {
             'gateway_name': i.gateway_name,
             'description': i.description,
             'sub_device': i.sub_device,
             'create_date': i.create_date.strftime('%Y-%m-%d')
            })
    return HttpResponse(json.dumps({'msg': 'ok', 'data': result}), content_type='application/json')




