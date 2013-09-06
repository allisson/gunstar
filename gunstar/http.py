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

    def before_dispatch(self):
        pass

    def dispatch(self, *args, **kwargs):
        # call before dispatch
        self.before_dispatch()
        
        # flag to control method not allowed error
        handler_executed = False

        if self.request.method.lower() in self.http_method_names:
            handler = getattr(self, self.request.method.lower(), None)
            if handler:
                handler_executed = True                
                handler(*args, **kwargs)

        if not handler_executed:
            self.abort(405, 'Method Not Allowed.')
        
        # call after dispatch
        self.after_dispatch()

    def after_dispatch(self):
        pass

    def abort(self, code, message=None):
        self.response.status_code = code
        if not message:
            message = 'Returned Status Code = {0}'.format(code)
        self.response.write(message)

    def redirect(self, redirect_url, permanent=False, status_code=302):
        message = 'The resource has been moved to {0}'.format(redirect_url)
        if permanent:
            status_code = 301
        self.response.status_code = status_code
        self.response.location = redirect_url
        self.response.write(message)

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

