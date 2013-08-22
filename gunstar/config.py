# -*- coding: utf-8 -*-
import six
from datetime import timedelta
from gunstar.utils import import_from_string


class DefaultConfig(object):
    
    DEBUG = True
    TESTING = False

    SECRET_KEY = ''
    SESSION_COOKIE_NAME = 'gsessionid'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    STATIC_ROOT = ''
    STATIC_PATH = ''

    HANDLER_FOR_404 = 'gunstar.http.NotFoundHandler'
    HANDLER_FOR_500 = 'gunstar.http.ErrorHandler'


class Config(dict):

    def load_from_object(self, obj):
        if isinstance(obj, six.string_types):
            obj = import_from_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
