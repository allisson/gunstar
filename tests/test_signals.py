# -*- coding: utf-8 -*-
from gunstar.app import Application
from gunstar.http import RequestHandler
from gunstar.testing import TestCase
from gunstar.signals import *
import os


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


class Handler1(RequestHandler):
    def get(self):
        self.response.write('handler1')


class Handler2(RequestHandler):
    def get(self):
        self.render_template('index.html', name='allisson')


class Handler3(RequestHandler):
    def get(self):
        self.reponse.write(var)


class Settings(object):

    SECRET_KEY = 'my-secret'
    TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


routes = (
    ('/handler1/', Handler1, 'handler1'),
    ('/handler2/', Handler2, 'handler2'),
    ('/handler3/', Handler3, 'handler3'),
)


class SignalsTest(TestCase):

    def get_app(self):
        self.app = Application(routes=routes, config=Settings)
        return self.app

    def test_request_started_signal(self):

        def receive_request_started_signal(app, request):
            self.signal_received = {
                'app': app, 'request': request
            }

        request_started_signal.connect(receive_request_started_signal)

        resp = self.client.get('/handler1/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertEqual(
            self.signal_received['request'].path_info,
            '/handler1/'
        )

        resp = self.client.get('/handler2/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertEqual(
            self.signal_received['request'].path_info,
            '/handler2/'
        )

        resp = self.client.get('/handler3/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertEqual(
            self.signal_received['request'].path_info,
            '/handler3/'
        )

    def test_request_finished_signal(self):

        def receive_request_finished_signal(app, response):
            self.signal_received = {
                'app': app, 'response': response
            }

        request_finished_signal.connect(receive_request_finished_signal)

        resp = self.client.get('/handler1/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertEqual(self.signal_received['response'].text, resp.text)

        resp = self.client.get('/handler2/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertEqual(self.signal_received['response'].text, resp.text)

    def test_request_exception_signal(self):

        def receive_request_exception_signal(app, request, exc_info):
            self.signal_received = {
                'app': app, 'request': request, 'exc_info': exc_info
            }

        request_exception_signal.connect(receive_request_exception_signal)

        resp = self.client.get('/handler3/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertEqual(
            self.signal_received['request'].path_info, '/handler3/'
        )
        self.assertTrue(self.signal_received['exc_info'])

    def test_template_rendered_signal(self):

        def receive_template_rendered_signal(app, handler, template, context):
            self.signal_received = {
                'app': app, 'handler': handler, 'template': template,
                'context': context
            }

        template_rendered_signal.connect(receive_template_rendered_signal)

        resp = self.client.get('/handler2/')
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_received['app'], self.app)
        self.assertTrue(
            isinstance(self.signal_received['handler'], RequestHandler)
        )
        self.assertEqual(self.signal_received['template'], resp.text)
        self.assertEqual(self.signal_received['context']['name'], 'allisson')
