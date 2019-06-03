import json
from django.http import HttpResponse
from .models import GatewayBase, MqttTopic
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


def mqtt_config(request):
    # data = json.loads(request.POST['data'])
    # print(data)
    try:
        with open('./config/mqtt_config.json', 'w', encoding='utf-8') as f:
            f.write(request.POST['data'])
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '修改失败'}), content_type='application/json')


def create_topic(request):
    mq = MqttTopic()
    try:
        mq.topic = request.POST['topic']
        mq.description = request.POST['description']
        mq.tag = request.POST['tag']
        mq.function = request.POST['function_des']
        mq.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '创建失败' + str(e)}), content_type='application/json')


def get_all_topic(request):
    all_topic = MqttTopic.objects.all()
    result = []
    for i in all_topic:
        result.append({
            'topic': i.topic,
            'function_des': i.function,
            'tag': i.tag,
            'description': i.description
        })
    return HttpResponse(json.dumps({'msg': 'ok', 'data': result}), content_type='application/json')


def del_topic(request):
    topic = request.POST['topic']
    try:
        MqttTopic.objects.filter(topic=topic).delete()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '删除失败' + str(e)}), content_type='application/json')


def edit_topic(request):
    try:
        before_edit = request.POST['before_edit']
        topic = MqttTopic.objects.get(topic=before_edit)
        topic.topic = request.POST['topic']
        topic.description = request.POST['description']
        topic.tag = request.POST['tag']
        topic.function = request.POST['function_des']
        topic.save()
        return HttpResponse(json.dumps({'msg': 'ok'}), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'msg': '修改失败' + str(e)}), content_type='application/json')
