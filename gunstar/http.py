# -*- coding: utf-8 -*-
import webob
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class Request(webob.request.Request):
    pass


class Response(webob.response.Response):

    def __init__(self, app=None, *args, **kwargs):
        self.app = app
        super(Response, self).__init__(*args, **kwargs)

    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.app.config.get('TEMPLATE_PATH', None):
            template_dirs.append(self.app.config['TEMPLATE_PATH'])
        env = Environment(loader=FileSystemLoader(template_dirs))
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        self.text = template.render(kwargs)


Request.ResponseClass = Response
Response.RequestClass = Request
