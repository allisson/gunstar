# -*- coding: utf-8 -*-
from gunstar.app import Application
import os


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


class ConfigSettings(object):
    
    TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
    SECRET_KEY = 'my-secret-key'
    STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
    STATIC_PATH = '/static/'


routes = (
    ('/', 'handlers.IndexHandler', 'index'),
    ('/name/{name}/', 'handlers.OtherHandler', 'other'),
)


app = Application(routes=routes, config=ConfigSettings)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8080, app)
    server.serve_forever()
