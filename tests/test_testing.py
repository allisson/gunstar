# -*- coding: utf-8 -*-
import six
import os
from gunstar.testing import TestCase
from gunstar.app import Application
from gunstar.http import RequestHandler


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


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


class SessionHandler(RequestHandler):

    def get(self):
        if self.session.get('name'):
            self.response.write('Get session name = {0}'.format(
                self.session.get('name'))
            )
        else:
            self.session.set('name', 'allisson')
            self.session.save()
            self.response.write('Set session name')


class SessionHandler2(RequestHandler):

    def get(self):
        self.session.clear()
        self.session.save()
        self.response.write('Session is gone')


class SessionHandler3(RequestHandler):

    def get(self):
        self.render_template('index.html', name='allisson')


routes = (
    ('/', Handler, 'index'),
    ('/session/', SessionHandler, 'session'),
    ('/session2/', SessionHandler2, 'session2'),
    ('/session3/', SessionHandler3, 'session3'),
)


class Settings(object):
    SECRET_KEY = 'my-secret'
    TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


class ClientTest(TestCase):

    def get_app(self):
        return Application(routes=routes, config=Settings)

    def test_get(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'GET')
        self.assertEqual(resp.request_started.path_qs, '/')

        resp = self.client.get('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'GET')
        self.assertEqual(resp.request_started.path_qs, '/?name=allisson')

        resp = self.client.get('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'GET')
        self.assertEqual(resp.request_started.headers['NAME'], 'allisson')

    def test_head(self):
        resp = self.client.head('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'HEAD')
        self.assertEqual(resp.request_started.path_qs, '/')

        resp = self.client.head('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'HEAD')
        self.assertEqual(resp.request_started.path_qs, '/?name=allisson')

        resp = self.client.head('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'HEAD')
        self.assertEqual(resp.request_started.headers['NAME'], 'allisson')

    def test_post(self):
        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'POST')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type,
            'application/x-www-form-urlencoded'
        )

        resp = self.client.post('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'POST')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.body, six.b('name=allisson'))
        self.assertEqual(
            resp.request_started.content_type,
            'application/x-www-form-urlencoded'
        )

        resp = self.client.post('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'POST')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.headers['NAME'], 'allisson')
        self.assertEqual(
            resp.request_started.content_type,
            'application/x-www-form-urlencoded'
        )

        resp = self.client.post('/', content_type='application/octet-stream')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'POST')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

    def test_put(self):
        resp = self.client.put('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'PUT')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

        resp = self.client.put('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'PUT')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.body, six.b('name=allisson'))
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

        resp = self.client.put('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'PUT')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.headers['NAME'], 'allisson')
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

        resp = self.client.put('/', content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'PUT')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type,
            'multipart/form-data'
        )

    def test_delete(self):
        resp = self.client.delete('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'DELETE')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

        resp = self.client.delete('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'DELETE')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.body, six.b('name=allisson'))
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

        resp = self.client.delete('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'DELETE')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.headers['NAME'], 'allisson')
        self.assertEqual(
            resp.request_started.content_type,
            'application/octet-stream'
        )

        resp = self.client.delete('/', content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'DELETE')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type,
            'multipart/form-data'
        )

    def test_options(self):
        resp = self.client.options('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'OPTIONS')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type, 'application/octet-stream'
        )

        resp = self.client.options('/', data={'name': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'OPTIONS')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.body, six.b('name=allisson'))
        self.assertEqual(
            resp.request_started.content_type, 'application/octet-stream'
        )

        resp = self.client.options('/', headers={'NAME': 'allisson'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'OPTIONS')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(resp.request_started.headers['NAME'], 'allisson')
        self.assertEqual(
            resp.request_started.content_type, 'application/octet-stream'
        )

        resp = self.client.options('/', content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request_started.method, 'OPTIONS')
        self.assertEqual(resp.request_started.path, '/')
        self.assertEqual(
            resp.request_started.content_type, 'multipart/form-data'
        )

    def test_load_and_store_cookies(self):
        self.assertFalse(self.client.cookies)

        resp = self.client.get('/session/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, six.b('Set session name'))
        self.assertTrue(self.client.cookies)
        self.assertTrue('gsessionid' in self.client.cookies)

        resp = self.client.get('/session/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, six.b('Get session name = allisson'))
        self.assertTrue(self.client.cookies)
        self.assertTrue('gsessionid' in self.client.cookies)

        resp = self.client.get('/session2/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, six.b('Session is gone'))
        self.assertTrue(self.client.cookies)

    def test_template_and_context_in_response(self):

        resp = self.client.get('/session3/')
        self.assertTrue(resp.template)
        self.assertTrue(resp.context)
        self.assertEqual(resp.template, resp.text)
        self.assertEqual(resp.context['name'], 'allisson')

        resp = self.client.get('/session2/')
        self.assertFalse(resp.template)
        self.assertFalse(resp.context)
