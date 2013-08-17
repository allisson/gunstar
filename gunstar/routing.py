# -*- coding: utf-8 -*-
import re
import six
from gunstar.utils import import_from_string


class Router(object):
    
    routes = ()

    def __init__(self, routes=None):
        if isinstance(routes, tuple):
            for route in routes:
                self.add_route(route[0], route[1], route[2])
        
    def add_route(self, pattern, func, name):
        self.routes += ( 
            Route(pattern, func, name), 
        )

    def find_route(self, path):
        for route in self.routes:
            match = re.search(route.pattern, path)
            if match:
                return route
        return None


class Route(object):
    
    def __init__(self, pattern, func, name):
        self.pattern = pattern
        self.func = func
        self.name = name
        
    def resolve_func(self):
        if isinstance(self.func, six.string_types):
            imported_func = import_from_string(self.func)
        elif six.callable(self.func):
            imported_func = self.func
        return imported_func
        
    def get_args_kwargs(self, path):
        match = re.search(self.pattern, path)
        kwargs = match.groupdict()
        if kwargs:
            args = ()
        else:
            args = match.groups()
        return args, kwargs
