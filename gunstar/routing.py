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
            match = re.search(route.regex_pattern, path)
            if match:
                return route
        return None

    def find_route_by_name(self, name):
        for route in self.routes:
            if route.name == name:
                return route
        return None


GET_TOKEN_RE = r'{([^}]+)}'
DEFAULT_TOKEN_RE = '([^/]+)'
INT_TOKEN_RE = '([\d]+)'
STRING_TOKEN_RE = '([\w]+)'
SLUG_TOKEN_RE = '([\w-]+)'
PATH_TOKEN_RE = '([^/].*?)'


class Route(object):
    
    def __init__(self, pattern, func, name):
        self.pattern = pattern
        self.func = func
        self.name = name
        self.regex_pattern = self.generate_regex_pattern()
        
    def resolve_func(self):
        imported_func = None
        if isinstance(self.func, six.string_types):
            imported_func = import_from_string(self.func)
        elif six.callable(self.func):
            imported_func = self.func
        return imported_func
        
    def get_args(self, path):
        match = re.search(self.regex_pattern, path)
        args = match.groups()
        return args

    def get_token_from_pattern(self):
        token_list = re.findall(GET_TOKEN_RE, self.pattern)
        return token_list

    def convert_token_to_regex(self, token):
        if len(token.split(':')) == 2:
            token_name, parser = token.split(':')
            if parser == 'int':
                return INT_TOKEN_RE
            elif parser == 'string':
                return STRING_TOKEN_RE
            elif parser == 'slug':
                return SLUG_TOKEN_RE
            elif parser == 'path':
                return PATH_TOKEN_RE
        elif len(token.split(':')) == 3:
            token_name, parser, options = token.split(':')
            if parser == 're':
                return options
        return DEFAULT_TOKEN_RE

    def generate_regex_pattern(self):
        regex_pattern = self.pattern
        token_list = self.get_token_from_pattern()
        for token in token_list:
            regex = self.convert_token_to_regex(token)
            regex_pattern = regex_pattern.replace('{%s}' % token, regex)
        return '^' + regex_pattern + '$'

    def reverse_route(self, *args):
        reversed_pattern = self.pattern
        token_list = self.get_token_from_pattern()
        if len(token_list) != len(args):
            return
        for i in range(len(token_list)):
            reversed_pattern = reversed_pattern.replace(
                '{%s}' % str(token_list[i]), str(args[i])
            )
        return reversed_pattern


