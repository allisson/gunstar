# -*- coding: utf-8 -*-
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from gunstar.session import Session


class RequestHandler(object):

    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def __init__(self, app, request, response):
        self.app = app
        self.request = request
        self.response = response
        self.session = Session(self.app, self.request, self.response)

    def dispatch(self, *args, **kwargs):
        if self.request.method.lower() in self.http_method_names:
            handler = getattr(self, self.request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(*args, **kwargs)

    def http_method_not_allowed(self, *args, **kwargs):
        self.response.status_code = 405
        self.response.write('Method Not Allowed.')

    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.app.config.get('TEMPLATE_PATH', None):
            template_dirs.append(self.app.config['TEMPLATE_PATH'])
        env = Environment(loader=FileSystemLoader(template_dirs))
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        self.response.text = template.render(kwargs)
