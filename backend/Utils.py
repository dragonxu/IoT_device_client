# coding: UTF-8

import time
import json
import os
import logging
from config import logging_config

_logging = logging.getLogger(__file__)


def getTS():
    '''
    获取毫秒单位的时间戳
    :return:
    '''
    return int(round(time.time() * 1000))


def parseArgs(args):
    '''
    命令行参数解析
    :param args:
    :return:
    '''
    conf = {}
    for v in args:
        if isinstance(v, str):
            if v.startswith("-"):
                data = v[1:].split("=")
                if len(data) == 2:
                    conf[data[0]] = data[1]
    return conf


def fileExist(file):
    return os.path.exists(file)


def readFile(file):
    '''
    读取文件
    :param file:
    :return:
    '''
    f = open(file)
    return f.read()


def readJsonFile(file):
    '''
    读取JSON文件
    :param file:
    :return:
    '''

    jsonFile = open(file)
    return json.load(jsonFile, encoding = "utf-8")


def jsonParse(jsonStr):
    return json.loads(jsonStr, encoding = "utf-8")


def toJsonString(obj):
    '''
    将对象变成JSON字符串
    :param obj:
    :return:
    '''
    return json.dumps(obj, ensure_ascii = False)


def log(msg, level = 'debug'):
    logging_config.initLogConf()
    try:
        level = level.lower()
        if level == 'debug':
            output_log(msg)
        elif level == 'info':
            logging.info(msg)
        elif level == 'warn':
            logging.warning(msg)
        elif level == 'error':
            logging.error(msg)
        else:
            logging.debug(msg)
    except BaseException:
        pass


def output_log(msg):
    logging_config.initOutputConf()
    logging.debug(msg)


if __name__ == '__main__':

    print(fileExist('config.json'))
