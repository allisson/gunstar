# -*- coding: utf-8 -*-
import six
from gunstar.testing import TestCase
from gunstar.app import Application
from gunstar.http import RequestHandler


class Handler(RequestHandler):
    
    def get(self):
        self.response.write('METHOD ={0}'.format(self.request.method))

    def post(self):
        self.response.write('METHOD ={0}'.format(self.request.method))

    def put(self):
        self.response.write('METHOD ={0}'.format(self.request.method))

    def delete(self):
        self.response.write('METHOD ={0}'.format(self.request.method))

    def options(self):
        self.response.write('METHOD ={0}'.format(self.request.method))

    def head(self):
        self.response.write('METHOD ={0}'.format(self.request.method))
    

routes = (
    (r'^$', Handler, 'index'),
)


app = Application(routes=routes)


class ClientTest(TestCase):

    def get_app(self):
        return app

    def test_get(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'GET')
        self.assertEqual(resp.req.path_qs, '/')

        resp = self.client.get('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'GET')
        self.assertEqual(resp.req.path_qs, '/?name=allisson')

        resp = self.client.get('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'GET')
        self.assertEqual(resp.req.headers['NAME'], 'allisson')

    def test_head(self):
        resp = self.client.head('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'HEAD')
        self.assertEqual(resp.req.path_qs, '/')

        resp = self.client.head('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'HEAD')
        self.assertEqual(resp.req.path_qs, '/?name=allisson')

        resp = self.client.head('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'HEAD')
        self.assertEqual(resp.req.headers['NAME'], 'allisson')

    def test_post(self):
        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'POST')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'multipart/form-data')

        resp = self.client.post('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'POST')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.body, six.b('name=allisson'))
        self.assertEqual(resp.req.content_type, 'multipart/form-data')

        resp = self.client.post('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'POST')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.headers['NAME'], 'allisson')
        self.assertEqual(resp.req.content_type, 'multipart/form-data')

        resp = self.client.post('/', content_type='application/octet-stream')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'POST')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

    def test_put(self):
        resp = self.client.put('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'PUT')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.put('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'PUT')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.body, six.b('name=allisson'))
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.put('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'PUT')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.headers['NAME'], 'allisson')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.put('/', content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'PUT')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'multipart/form-data')

    def test_delete(self):
        resp = self.client.delete('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'DELETE')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.delete('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'DELETE')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.body, six.b('name=allisson'))
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.delete('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'DELETE')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.headers['NAME'], 'allisson')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.delete('/', content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'DELETE')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'multipart/form-data')

    def test_options(self):
        resp = self.client.options('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'OPTIONS')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.options('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'OPTIONS')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.body, six.b('name=allisson'))
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.options('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'OPTIONS')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.headers['NAME'], 'allisson')
        self.assertEqual(resp.req.content_type, 'application/octet-stream')

        resp = self.client.options('/', content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.req.method, 'OPTIONS')
        self.assertEqual(resp.req.path, '/')
        self.assertEqual(resp.req.content_type, 'multipart/form-data')
