# -*- coding: utf-8 -*-
import modbus_config


class Dict(dict):
    def __init__(self, names = (), values = (), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    # def __missing__(self, key):
    #     value = self[key] = type(self)()
    #     return value


def merge(default, override):
    r = override
    for k, v in default.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


configs = modbus_config.configs

try:
    import config.mqtt_config as mqtt_config
    import config.bash_config as bash_config

    configs = merge(configs, mqtt_config.configs)
    configs = merge(configs, bash_config.configs)
except ImportError:
    pass

configs = toDict(configs)
if __name__ == '__main__':
    print(configs)
