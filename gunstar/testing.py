# -*- coding: utf-8 -*-
import unittest
import six
from gunstar.http import Request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


BOUNDARY = 'BoUnDaRyStRiNg'
MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY


class Client(object):

    def __init__(self, app):
        self.app = app

    def get(self, path, data={}, headers={}):
        return self.get_request(path, data=data, headers=headers)

    def post(self, path, data={}, headers={}, content_type=MULTIPART_CONTENT):
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
        resp = req.get_response(self.app)
        resp.req = req
        return resp

    def post_request(self, path, data={}, headers={}, content_type='', method='POST'):
        req = Request.blank(path)
        req.content_type = content_type
        req.method = method
        req.body = six.b(urlencode(data))
        req.headers.update(headers)
        resp = req.get_response(self.app)
        resp.req = req
        return resp


class TestCase(unittest.TestCase):

    def get_app(self):
        raise NotImplementedError()

    def __call__(self, result=None):
        self.client = Client(self.get_app())
        super(TestCase, self).__call__(result)

