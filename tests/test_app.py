# -*- coding: utf-8 -*-
import unittest
import os
from gunstar.app import Application
from gunstar.routing import Router
from gunstar.config import Config
from gunstar.http import Request, Response


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


class TestConfig(object):

    KEY1 = 'key1'
    key2 = 'key2'
    STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
    STATIC_PATH = '/static/'


class ApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Application()

    def test_init(self):
        self.assertTrue(
            isinstance(self.app.router, Router)
        )

        self.assertTrue(
            isinstance(self.app.config, Config)
        )

    def load_config(self):
        self.app.load_config(TestConfig)
        self.assertTrue('KEY1' in self.app.config)
        self.assertFalse('key2' in self.app.config)

    def test_add_route(self):
        self.app.add_route('/test/', 'handlers.TestHandler', 'test')
        self.assertTrue(self.app.router.find_route('/test/'))

    def test_call(self):
        req = Request.blank('/article?id=1')

        resp = req.get_response(self.app)
        self.assertTrue(isinstance(resp, Response))
        self.assertEqual(resp.status_code, 404)
        self.assertTrue('Not Found /article' in resp.text)
