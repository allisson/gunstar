# -*- coding: utf-8 -*-
from gunstar.app import Application
import os.path


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


config = {
    'TEMPLATE_PATH': os.path.join(PROJECT_PATH, 'templates')
}


routes = (
    (r'^$', 'views.index', 'index'),
    (r'^name/([\w:-]+)/$', 'views.other', 'other'),
)


app = Application(routes=routes, config=config)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8080, app)
    server.serve_forever()
