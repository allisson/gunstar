# -*- coding: utf-8 -*-
from gunstar.http import Request, Response, DirectoryApp
from gunstar.routing import Router
from gunstar.config import Config, DefaultConfig
import six


class Application(object):

    def __init__(self, routes=None, config=None):
        
        self.router = Router(routes)
        self.config = Config()
        self.config.load_from_object(DefaultConfig)
        self.config.load_from_object(config)

        # add static dir route
        self.static_root = self.config.get('STATIC_ROOT')
        self.static_path = self.config.get('STATIC_PATH')
        if self.static_root and self.static_path:
            self.router.add_route(
                self.static_path + '{file:path}',
                DirectoryApp,
                'static'
            )

    def load_config(self, config):
        self.config.load_from_object(config)

    def __call__(self, environ, start_response):
        self.request = Request(environ)
        self.response = Response()
        path = self.request.path_info
        route = self.router.find_route(path)
        if route:
            func = route.resolve_func()
            # check is route for static files
            if route.name == 'static':
                static_handler = func(self.static_root)
                self.request.path_info = self.request.path_info.replace(self.static_path, '')
                resp = self.request.get_response(static_handler)
                return resp(environ, start_response)
            args = route.get_args(path)
            handler = func(self, self.request, self.response)
            handler.dispatch(*args)
            return handler.response(environ, start_response)
        else:
            self.response.status = 404
            self.response.text = six.u('Not Found.')
        return self.response(environ, start_response)
