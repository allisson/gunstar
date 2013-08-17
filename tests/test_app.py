# -*- coding: utf-8 -*-
import unittest
from gunstar.app import Application
from gunstar.routing import Router
from gunstar.config import Config
from gunstar.http import Request, Response


class ApplicationTestCase(unittest.TestCase):
    
    def test_init(self):
        app = Application()
        
        self.assertTrue(
            isinstance(app.router, Router)
        )

        self.assertTrue(
            isinstance(app.config, Config)
        )

    def test_call(self):
        app = Application()
        req = Request.blank('/article?id=1')

        resp = req.get_response(app)
        self.assertTrue(isinstance(resp, Response))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.text, 'Not Found.')
