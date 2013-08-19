# -*- coding: utf-8 -*-
from gunstar.http import Request, Response
from gunstar.routing import Router
from gunstar.config import Config, DefaultConfig
import six


class Application(object):

    def __init__(self, routes=None, config=None):
        
        self.router = Router(routes)
        self.config = Config()
        self.config.load_from_object(DefaultConfig)
        self.config.load_from_object(config)

    def load_config(self, config):
        self.config.load_from_object(config)

    def __call__(self, environ, start_response):
        self.request = Request(environ)
        self.response = Response()
        path = self.request.path_info.lstrip('/')
        route = self.router.find_route(path)
        if route:
            func = route.resolve_func()
            args, kwargs = route.get_args_kwargs(path)
            handler = func(self, self.request, self.response)
            handler.dispatch(*args, **kwargs)
            return handler.response(environ, start_response)
        else:
            self.response.status = 404
            self.response.text = six.u('Not Found.')
        return self.response(environ, start_response)
