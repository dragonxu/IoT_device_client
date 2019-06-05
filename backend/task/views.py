import json
from django.http import HttpResponse
from django.utils import timezone
from .models import Gateway_task, TaskRecord
from gateway.models import GatewayBase
# Create your views here.


def get_all(request):
    all_task = Gateway_task.objects.all()
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
    task = Gateway_task()
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
            Gateway_task.objects.filter(name=i).delete()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '删除失败' + str(e)}), content_type='application/json')


def edit(request):
    try:
        before_edit = request.POST['before_edit']
        task = Gateway_task.objects.get(name=before_edit)
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '修改失败'}), content_type='application/json')


def change_status(request):
    pass


def add_record(request):
    record = TaskRecord()
    print(request.POST)
    try:
        record.gateway = GatewayBase.objects.get(gateway_name=request.POST['gateway'])
        record.slave_id = request.POST['slave_id']
        record.function_name = request.POST['function_name']
        record.identifier = request.POST['identifier']
        record.modbus_function_code = request.POST['modbus_function_code']
        record.start_address = request.POST['start_address']
        record.data_length = request.POST['data_length']
        record.top_limit = request.POST['top_limit']
        record.low_limit = request.POST['low_limit']
        record.scale = request.POST['scale']
        record.interval = request.POST['interval']
        record.send_way = request.POST['send_way']
        record.compute = request.POST['compute']
        record.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '添加失败'+str(e)}), content_type='application/json')



