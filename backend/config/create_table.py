import json
from devices.models import Attribute


category = ['水浸传感器', '水浸检测', '烟雾报警器', '电表', '多功能电表', '电力仪表', '烟感传感器',
            '温湿度采集单元', '室内温度传感器', '室内温湿度监测设备', '智能电表', '危险报警器', '报警开关', '寄存器', ]

with open('attribute.json') as f:
    data = json.loads(f.read())

for i in data:
    if i['CategoryName'] in category:
        Attribute.objects.create(name=i['Name'], identifier=i['Identifier'], category=i['CategoryName'],
                                 code=i['AbilityId'])
