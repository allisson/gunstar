# -*- coding: utf-8 -*-
import unittest
import os
from gunstar.http import Request, Response, RequestHandler
from gunstar.app import Application
from gunstar.session import Session


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


class ConfigSettings(object):    
    TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


app = Application(config=ConfigSettings)


class Handler(RequestHandler):

    def get(self):
        self.render_template('index.html')


class RequestHandlerTest(unittest.TestCase):

    def setUp(self):
        self.request = Request.blank('/')
        self.response = Response()
        self.handler = Handler(app, self.request, self.response)

    def test_render_template(self):
        self.handler.dispatch()
        self.assertTrue('<h1>Index Page</h1>' in self.handler.response.text)

    def test_has_session(self):
        self.assertTrue(isinstance(self.handler.session, Session))
