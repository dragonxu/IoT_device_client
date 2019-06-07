# -*- conding:utf-8 -*-
import datetime
import logging
import logging.config
import os


def genLogDict(logDir, logFile):
    '''
    配置日志格式的字典
    '''
    logDict = {
        "version": 1,
        "disable_existing_loggers": False,
        # 日志输出格式设置
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },

        "handlers": {
            # 控制台处理器,控制台输出
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            # 默认处理器,打印到文件
            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": os.path.join(logDir, logFile),
                'mode': 'w+',
                "maxBytes": 1024 * 1024 * 10,  # 10 MB
                "backupCount": 20,
                "encoding": "utf8"
            },
        },
        "root": {
            'handlers': ['default', 'console'],
            'level': "DEBUG",
            'propagate': False
        }
    }
    return logDict


def initLogConf():
    """
    配置日志
    """
    baseDir = os.path.dirname(os.path.abspath(__file__))
    logDir = os.path.join(baseDir, "../runtime/logs")
    if not os.path.exists(logDir):
        os.makedirs(logDir)  # 创建路径

    logFile = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    logDict = genLogDict(logDir, logFile)
    logging.config.dictConfig(logDict)


def initOutputConf():
    """
    配置日志
    """
    baseDir = os.path.dirname(os.path.abspath(__file__))
    logDir = os.path.join(baseDir, "../runtime/logs/output")
    if not os.path.exists(logDir):
        os.makedirs(logDir)  # 创建路径

    logFile = "output.log"
    logDict = genLogDict(logDir, logFile)
    logging.config.dictConfig(logDict)
