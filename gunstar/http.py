# -*- coding: utf-8 -*-
from webob import Request, Response
from webob.static import DirectoryApp
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import traceback
from gunstar.session import Session
from gunstar.template import linebreaks, linebreaksbr
from gunstar.signals import template_rendered_signal
import os.path


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
GUNSTAR_TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


class RequestHandler(object):

    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def __init__(self, app, request, response):
        self.app = app
        self.request = request
        self.response = response
        self.session = Session(self.app, self.request, self.response)
        self.template_env = self.create_template_env()

    def dispatch(self, *args, **kwargs):
        if self.request.method.lower() in self.http_method_names:
            handler = getattr(self, self.request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(*args, **kwargs)

    def http_method_not_allowed(self, *args, **kwargs):
        self.response.status_code = 405
        self.response.write('Method Not Allowed.')

    def get_template_globals(self):
        template_globals = {
            'handler': self,
            'config': self.app.config,
            'request': self.request,
            'reverse_route': self.reverse_route,
        }
        return template_globals

    def get_template_filters(self):
        template_filters = {'linebreaks': linebreaks, 'linebreaksbr': linebreaksbr}
        return template_filters

    def create_template_env(self):
        template_dirs = []
        if self.app.config.get('TEMPLATE_PATH', None):
            template_dirs.append(self.app.config['TEMPLATE_PATH'])
        template_dirs.append(GUNSTAR_TEMPLATE_PATH)
        template_env = Environment(
            loader=FileSystemLoader(template_dirs),
            extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_'],
            autoescape=True
        )
        template_env.globals.update(self.get_template_globals())
        template_env.filters.update(self.get_template_filters())
        return template_env

    def render_template(self, template_name, **kwargs):
        try:
            template = self.template_env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        template_rendered = template.render(kwargs)
        template_rendered_signal.send(
            self.app, handler=self, template=template_rendered, context=kwargs
        )
        self.response.text = template_rendered

    def reverse_route(self, name, *args):
        url = ''
        route = self.app.router.find_route_by_name(name)
        if route:
            reverse = route.reverse_route(*args)
            if reverse:
                url = reverse
        return url



class NotFoundHandler(RequestHandler):

    def get(self):
        self.response.status = 404
        self.render_template('404.html', path=self.request.path_info)


class ErrorHandler(RequestHandler):

    def get(self, exc_info):
        self.response.status = 500
        self.render_template('500.html', traceback=traceback.format_exception(*exc_info))

