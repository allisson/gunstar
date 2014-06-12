# -*- coding: utf-8 -*-
import unittest
import os
from jinja2 import TemplateNotFound

from gunstar.http import Request, Response, RequestHandler
from gunstar.app import Application
from gunstar.session import Session


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


class ConfigSettings(object):
    TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


app = Application(config=ConfigSettings)


class Handler(RequestHandler):

    def get(self):
        self.render_template('index.html', message='My big\nMessage!')


class TemplateNotFoundHandler(RequestHandler):

    def get(self):
        self.render_template('not-found-template.html')


class AbortHandler(RequestHandler):

    def get(self):
        self.abort(404, message='Not Found.')

    def post(self):
        self.abort(404)


class RedirectHandler(RequestHandler):

    def get(self):
        self.redirect('http://gunstar.readthedocs.org')


class RedirectPermanentHandler(RequestHandler):

    def get(self):
        self.redirect('http://gunstar.readthedocs.org', permanent=True)


class RedirectWithOtherCodeHandler(RequestHandler):

    def get(self):
        self.redirect('http://gunstar.readthedocs.org', status_code=307)


class RequestHandlerTest(unittest.TestCase):

    def setUp(self):
        self.request = Request.blank('/')
        self.response = Response()
        self.app = app

    def test_render_template(self):
        handler = Handler(self.app, self.request, self.response)
        handler.dispatch()
        self.assertTrue('<h1>Index Page</h1>' in handler.response.text)

    def test_render_template_not_found(self):
        handler = TemplateNotFoundHandler(
            self.app, self.request, self.response
        )
        self.assertRaises(TemplateNotFound, lambda: handler.dispatch())

    def test_has_session(self):
        handler = Handler(self.app, self.request, self.response)
        self.assertTrue(isinstance(handler.session, Session))

    def test_abort(self):
        handler = AbortHandler(self.app, self.request, self.response)
        handler.dispatch()
        self.assertEqual(handler.response.status_code, 404)
        self.assertEqual(handler.response.text, 'Not Found.')

    def test_abort_without_message(self):
        self.request.method = 'POST'
        handler = AbortHandler(self.app, self.request, self.response)
        handler.dispatch()
        self.assertEqual(handler.response.status_code, 404)
        self.assertEqual(handler.response.text, 'Returned Status Code = 404')

    def test_method_not_allowed(self):
        self.request.method = 'POST'
        handler = Handler(self.app, self.request, self.response)
        handler.dispatch()
        self.assertEqual(handler.response.status_code, 405)
        self.assertEqual(handler.response.text, 'Method Not Allowed.')

    def test_redirect(self):
        handler = RedirectHandler(self.app, self.request, self.response)
        handler.dispatch()
        self.assertEqual(handler.response.status_code, 302)
        self.assertEqual(
            handler.response.text,
            'The resource has been moved to http://gunstar.readthedocs.org'
        )

    def test_permanent_redirect(self):
        handler = RedirectPermanentHandler(
            self.app, self.request, self.response
        )
        handler.dispatch()
        self.assertEqual(handler.response.status_code, 301)
        self.assertEqual(
            handler.response.text,
            'The resource has been moved to http://gunstar.readthedocs.org'
        )

    def test_redirect_with_other_code(self):
        handler = RedirectWithOtherCodeHandler(
            self.app, self.request, self.response
        )
        handler.dispatch()
        self.assertEqual(handler.response.status_code, 307)
        self.assertEqual(
            handler.response.text,
            'The resource has been moved to http://gunstar.readthedocs.org'
        )

    def test_reverse_route(self):
        self.app.add_route('/', Handler, 'index')
        self.app.add_route('/index2/', Handler, 'index2')
        handler = Handler(
            self.app, self.request, self.response
        )
        self.assertEqual(
            handler.reverse_route('index'),
            '/'
        )
        self.assertEqual(
            handler.reverse_route('index2'),
            '/index2/'
        )
