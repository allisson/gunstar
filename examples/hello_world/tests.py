# -*- coding: utf-8 -*-
import unittest
from gunstar.http import Request
from app import app


class AppTestCase(unittest.TestCase):
    

    def test_handlers(self):
        req = Request.blank('/')
        resp = req.get_response(app)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<h1>Hello Gunstar!</h1>'in resp.text)

        req = Request.blank('/name/allisson/')
        resp = req.get_response(app)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<h1>Hello allisson!</h1>'in resp.text)

        req = Request.blank('/crazy/url/')
        resp = req.get_response(app)
        self.assertEqual(resp.status_code, 404)
        self.assertTrue('Not Found.' in resp.text)
