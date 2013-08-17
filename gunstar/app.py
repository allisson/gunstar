# -*- coding: utf-8 -*-
from gunstar.http import Request, Response
from gunstar.routing import Router
from gunstar.config import Config
import six


class Application(object):

    def __init__(self, routes=None, config=None):
        
        self.router = Router(routes)
        self.config = Config(config)

    def __call__(self, environ, start_response):
        self.req = Request(environ)
        self.res = Response(self)
        path = self.req.path_info.lstrip('/')
        route = self.router.find_route(path)
        if route:
            func = route.resolve_func()
            args, kwargs = route.get_args_kwargs(path)
            result = func(self.req, self.res, *args, **kwargs)
            return result(environ, start_response)
        else:
            self.res.status = 404
            self.res.text = six.u('Not Found.')
        return self.res(environ, start_response)
