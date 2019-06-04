import json
from django.http import HttpResponse
from django.utils import timezone
from .models import Task
from gateway.models import GatewayBase
# Create your views here.


def get_all(request):
    all_task = Task.objects.all()
    result = []
    for i in all_task:
        result.append({
            'name': i.name,
            'protocol': i.protocol,
            'description': i.description,
            'gateway': i.gateway.gateway_name,
            'create_time': i.create_time.strftime('%Y-%m-%d'),
            'status': 'true' if i.status else 'false'
        })
    return HttpResponse(json.dumps({'msg': 'ok', 'data': result}), content_type='application/json')


def create(request):
    task = Task()
    try:
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.create_time = timezone.datetime.now()
        task.protocol = 'Modbus'
        task.gateway = GatewayBase.objects.get(gateway_name=request.POST['gateway'])
        task.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '创建失败'}), content_type='application/json')


def delete(request):
    name = request.POST['name']
    try:
        name = name.split(',')
        for i in name:
            Task.objects.filter(name=i).delete()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '删除失败' + str(e)}), content_type='application/json')


def edit(request):
    try:
        before_edit = request.POST['before_edit']
        task = Task.objects.get(name=before_edit)
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '修改失败'}), content_type='application/json')


def change_status(request):
    pass
