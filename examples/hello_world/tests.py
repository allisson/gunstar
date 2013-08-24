# -*- coding: utf-8 -*-
from gunstar.testing import TestCase
from app import app


class AppTestCase(TestCase):
    
    def get_app(self):
        return app

    def test_handlers(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<h1>Hello!</h1>'in resp.text)

        resp = self.client.get('/name/allisson/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<h1>Hello allisson!</h1>' in resp.text)
        self.assertTrue(resp.context['name'], 'allisson')

        resp = self.client.get('/static/index.html')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<h1>Hello from static</h1>' in resp.text)

        resp = self.client.get('/crazy/url/')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue('Not Found /crazy/url/' in resp.text)
