# -*- coding: utf-8 -*-
from importlib import import_module


def import_from_string(import_string):
    if '.' in import_string:
        mod_str, func_str = import_string.rsplit('.', 1)
    else:
        return __import__(import_string)
    mod = import_module(mod_str)
    try:
        func = getattr(mod, func_str)
        return func
    except:
        return import_module(import_string)

