# -*- coding: utf-8 -*-
import six
from gunstar.utils import import_from_string


class Config(dict):

    def __init__(self, conf=None):
        if isinstance(conf, dict):
            for key in conf:
                if key.isupper():
                    self[key] = conf[key]

    def load_from_object(self, obj):
        if isinstance(obj, six.string_types):
            obj = import_from_string(obj)
            print obj
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
