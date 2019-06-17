# coding: UTF-8

from paho.mqtt import client as mqtt
import Utils

#网关遥测数据 TOPIC
_GATEWAY_TELEMETRY_TOPIC = "v1/gateway/telemetry"

#网关设备链接 TOPIC
_GATEWAY_DEVICE_CONNECT = "v1/gateway/connect"

#网关设备断开链接 TOPIC
_GATEWAY_DEVICE_DISCONNECT = "v1/gateway/disconnect"

#网关更新设备属性 TOPIC
_GATEWAY_DEVICE_ATTRIBUTES = "v1/gateway/attributes"

#网关获取设备属性 TOPIC
_GATEWAY_DEVICE_ATTRIBUTES_REQUEST = "v1/gateway/attributes/request"

#网关获取设备属性返回 TOPIC
_GATEWAY_DEVICE_ATTRIBUTES_RESPONSE = "v1/gateway/attributes/response"

#网关订阅设备属性更新 TOPIC
_GATEWAY_DEVICE_ATTRIBUTES_UPDATE = "v1/gateway/attributes"

#网关被调用 TOPIC
_GATEWAY_RPC = "v1/gateway/rpc"


_client = mqtt.Client()

_content = {}

def _onConnection(client, userdata, flags, rc):
    Utils.log("connection success")
    client.subscribe(_GATEWAY_DEVICE_ATTRIBUTES_UPDATE)
    client.subscribe(_GATEWAY_RPC)
    client.subscribe(_GATEWAY_DEVICE_ATTRIBUTES_RESPONSE)

    if "init" not in _content:
        func = _content['handler']['onConnectionCallback']
        func()
        _content['init'] = True


def _onMessage(client, userdata, msg):
    topic = msg.topic
    payload = str(msg.payload)
    if topic == _GATEWAY_DEVICE_ATTRIBUTES_UPDATE:          #属性更新
        obj = Utils.jsonParse(payload)
        _content['handler']['onAttributeUpdateCallback'](obj['device'], obj['data'])
    elif topic == _GATEWAY_DEVICE_ATTRIBUTES_RESPONSE:        #请求属性返回结果
        obj = Utils.jsonParse(payload)
        data = {}
        for key,val in obj.items():
            if key != "id" and key != 'device':
                data[key] = val
        device = obj['device'] if "device" in obj else ""
        _content['handler']['onAttributeRespCallback'](device, data)
    elif topic == _GATEWAY_RPC:                             #服务器对网关RPC调用
        obj = Utils.jsonParse(payload)
        func = _content['handler']['onRpcCallback']
        result = func(obj['device'], obj['data']['method'], obj['data']['params'])
        _client.publish(_GATEWAY_RPC, Utils.toJsonString({"device": obj['device'], "id": obj['data']['id'], "data":result}))
    else:
        Utils.log("unknow topic " + msg.topic, 'error')

def _onDisconnect(client, userdata, rc):
    Utils.log("connection disconnect")

def SendTelemetry(data, needToJson=True):
    '''
    发送遥测数据
    :param data:
    :param needToJson 是否需要做JSON编码
    :return:
    '''
    _client.publish(_GATEWAY_TELEMETRY_TOPIC, Utils.toJsonString(data) if needToJson else data)

def OnDeviceConnection(device):
    '''
    设备链接网关
    :return:
    '''

    _client.publish(_GATEWAY_DEVICE_CONNECT, Utils.toJsonString({"device": device}))

def OnDeviceDisconnection(device):
    '''
    设备链接网关断开
    :param device:
    :return:
    '''
    _client.publish(_GATEWAY_DEVICE_DISCONNECT, Utils.toJsonString({"device": device}))

def PushDeviceAttributes(device, attributes):
    '''
    设备属性发布到服务器
    :param device:
    :param aattributes:
    :return:
    '''
    _client.publish(_GATEWAY_DEVICE_ATTRIBUTES, Utils.toJsonString({device: attributes}))


def GetDeviceAttribute(device, attribute):
    '''
    从服务器获取设备属性
    :param device:
    :return:
    '''
    id = Utils.getTS()
    _client.publish(_GATEWAY_DEVICE_ATTRIBUTES_REQUEST, Utils.toJsonString({"id": id, "device": device, "client":False, "key": attribute}))


def Connection(host, port, token, handler):
    _client.username_pw_set(token)
    _client.on_connect = _onConnection
    _client.on_message = _onMessage
    _client.on_disconnect = _onDisconnect
    _client.connect(host,port)
    _content['handler'] = handler

def start():
    _client.loop_start()
