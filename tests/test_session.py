# -*- coding: utf-8 -*-
from six.moves import http_cookies

from gunstar.app import Application
from gunstar.session import Session
from gunstar.http import RequestHandler, Request, Response
from gunstar.testing import TestCase


class Handler(RequestHandler):

    def get(self):
        self.session.set('name', 'allisson')
        self.session.save()
        self.response.write('Hello')


class Handler2(RequestHandler):

    def get(self):
        self.response.write('Hello {0}'.format(self.session.get('name')))


class Settings(object):

    SECRET_KEY = 'my-secret'


routes = (
    ('/', Handler, 'index'),
    ('/index2/', Handler2, 'index2'),
)


app = Application(routes=routes, config=Settings)


class SessionTest(TestCase):

    def get_app(self):
        self.app = Application(routes=routes, config=Settings)
        return self.app

    def load_cookie(self, resp):
        cookie = http_cookies.SimpleCookie()
        try:
            cookie.load(resp.headers['Set-Cookie'])
            return cookie
        except KeyError:
            return None

    def test_get_cookie_domain(self):
        resp = self.client.get('/')
        cookie = self.load_cookie(resp)
        self.assertTrue('gsessionid' in cookie)
        self.assertEqual(
            cookie['gsessionid']['domain'],
            'localhost'
        )

        self.app.config['SESSION_COOKIE_DOMAIN'] = 'gunstar.github.io'

        resp = self.client.get('/')
        cookie = self.load_cookie(resp)
        self.assertTrue('gsessionid' in cookie)
        self.assertEqual(
            cookie['gsessionid']['domain'],
            'gunstar.github.io'
        )

    def test_get_session(self):
        self.app.config['SECRET_KEY'] = ''
        resp = self.client.get('/')
        self.assertFalse(resp.headers.get('Set-Cookie'))

        self.app.config['SECRET_KEY'] = 'my-secret'
        resp = self.client.get('/')
        cookie = self.load_cookie(resp)
        self.assertTrue('gsessionid' in cookie)

        self.client.cookies['gsessionid'] = 'invalid-cookie'
        resp = self.client.get('/index2/')
        self.assertEqual(resp.text, 'Hello None')
        cookie = self.load_cookie(resp)
        self.assertFalse(cookie)

    def test_get_set_clear_delete(self):
        request = Request.blank('/')
        response = Response()
        session = Session(self.app, request, response)

        self.assertFalse(session.get('name'))
        session.set('name', 'allisson')
        self.assertTrue(session.get('name'))
        session.delete('name')
        self.assertFalse(session.get('name'))
        session.set('name', 'allisson')
        session.set('age', 30)
        session.clear()
        self.assertFalse(session.get('name'))
        self.assertFalse(session.get('age'))
