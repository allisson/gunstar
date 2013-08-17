# -*- coding: utf-8 -*-
import unittest
import os
from gunstar.app import Application
from gunstar.http import Response


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
config = {
    'TEMPLATE_PATH': os.path.join(PROJECT_PATH, 'templates')
}
app = Application(config=config)


class ResponseTestCase(unittest.TestCase):
    
    def test_render_template(self):
        resp = Response(app)
        self.assertFalse(resp.text)
        resp.render_template('index.html')
        self.assertTrue(resp.text)
        self.assertTrue('<h1>Index Page</h1>' in resp.text)
