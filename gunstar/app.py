# -*- coding: utf-8 -*-
from gunstar.http import Request, Response, DirectoryApp
from gunstar.routing import Router
from gunstar.config import Config, DefaultConfig
from gunstar.utils import import_from_string
from gunstar.signals import (
    request_started_signal, request_finished_signal, request_exception_signal
    )
import sys


class Application(object):

    def __init__(self, routes=None, config=None):
        # set router
        self.router = Router(routes)

        # set config
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

        # handlers for 404 and 500
        self.handler404 = import_from_string(self.config.get('HANDLER_FOR_404'))
        self.handler500 = import_from_string(self.config.get('HANDLER_FOR_500'))

    def load_config(self, config):
        self.config.load_from_object(config)

    def add_route(self, pattern, handler, name):
        self.router.add_route(pattern, handler, name)

    def __call__(self, environ, start_response):
        self.request = Request(environ)
        request_started_signal.send(self, request=self.request)
        self.response = Response()
        path = self.request.path_info
        route = self.router.find_route(path)
        if route:
            try:
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
                request_finished_signal.send(self, response=handler.response)
                return handler.response(environ, start_response)
            except Exception:
                exc_info=sys.exc_info()
                request_exception_signal.send(self, request=self.request, exc_info=exc_info)
                handler_500 = self.handler500(self, self.request, self.response)
                handler_500.dispatch(exc_info)
                return handler_500.response(environ, start_response)
        else:
            handler_404 = self.handler404(self, self.request, self.response)
            handler_404.dispatch()
            return handler_404.response(environ, start_response)
