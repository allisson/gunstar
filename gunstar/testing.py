# -*- coding: utf-8 -*-
import unittest
import six
from six.moves import http_cookies
from gunstar.http import Request
from gunstar.signals import template_rendered_signal

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Client(object):

    def __init__(self, app):
        self.app = app
        self.cookies = {}
        self.template = None
        self.context = None
        template_rendered_signal.connect(self.receive_template_rendered_signal)

    def get(self, path, data={}, headers={}):
        return self.get_request(path, data=data, headers=headers)

    def post(self, path, data={}, headers={}, content_type='application/x-www-form-urlencoded'):
        return self.post_request(path, data=data, headers=headers, 
            content_type=content_type, method='POST')

    def put(self, path, data={}, headers={}, content_type='application/octet-stream'):
        return self.post_request(path, data=data, headers=headers, 
            content_type=content_type, method='PUT')

    def delete(self, path, data={}, headers={}, content_type='application/octet-stream'):
        return self.post_request(path, data=data, headers=headers, 
            content_type=content_type, method='DELETE')

    def options(self, path, data={}, headers={}, content_type='application/octet-stream'):
        return self.post_request(path, data=data, headers=headers, 
            content_type=content_type, method='OPTIONS')

    def head(self, path, data={}, headers={}):
        return self.get_request(path, data=data, headers=headers, method='HEAD') 

    def get_request(self, path, data={}, headers={}, method='GET'):
        if data:
            path = path + '?' + urlencode(data)
        req = Request.blank(path)
        req.method = method
        req.headers.update(headers)
        self.load_cookies(req)
        resp = req.get_response(self.app)
        self.store_cookies(resp)
        resp.request_started = req
        resp.template = self.template
        resp.context = self.context
        self.template = self.context= None
        return resp

    def post_request(self, path, data={}, headers={}, content_type='', method='POST'):
        req = Request.blank(path)
        req.content_type = content_type
        req.method = method
        req.body = six.b(urlencode(data))
        req.headers.update(headers)
        self.load_cookies(req)
        resp = req.get_response(self.app)
        self.store_cookies(resp)
        resp.request_started = req
        resp.template = self.template
        resp.context = self.context
        self.template = self.context= None
        return resp

    def store_cookies(self, resp):
        cookies = http_cookies.SimpleCookie()
        try:
            cookies.load(resp.headers['Set-Cookie'])
            for key in cookies:
                self.cookies[key] = cookies[key].value
        except:
            pass

    def load_cookies(self, req):
        for key in self.cookies:
            req.cookies[key] = self.cookies[key]

    def receive_template_rendered_signal(self, app, handler, template, context):
        self.template = template
        self.context = context


class TestCase(unittest.TestCase):

    def get_app(self):
        raise NotImplementedError()

    def _pre_setup(self):
        self.app = self.get_app()
        self.client = Client(self.app)

    def __call__(self, result=None):
        self._pre_setup()
        super(TestCase, self).__call__(result)

