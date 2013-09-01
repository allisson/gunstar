Testing
============

Gunstar has a TestCase, Subclass of unittest.TestCase with additional support for testing.

You have to implement the method get_app() in your TestCase.

Example:

.. code-block:: python

    # file app.py
    # -*- coding: utf-8 -*-
    from gunstar.app import Application
    from gunstar.http import RequestHandler
    import os


    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


    class ConfigSettings(object):

        TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


    class IndexHandler(RequestHandler):

        def get(self):
            self.render_template('index.html', title='index')


    routes = (
        ('/', IndexHandler, 'index'),
    )

    myapp = Application(routes=routes, config=ConfigSettings)


.. code-block:: python

    # file tests.py
    # -*- coding: utf-8 -*-
    from gunstar.testing import TestCase
    from app import myapp


    class IndexHandlerTest(TestCase):

        def get_app(self):
            return myapp

        def test_get(self):
            # test status code
            resp = self.client.get('/')
            self.assertEqual(resp.status_code, 200)

            # resp.request_started is the request that originated the response
            self.assertEqual(resp.request_started.method, 'GET')
            self.assertEqual(resp.request_started.path_qs, '/')

            # resp.template has the string rendered by template
            # resp.context has the context passed to render_template
            self.assertEqual(resp.text, resp.template)
            self.assertEqual(resp.context['title'], 'index')

            # request with parameters
            resp = self.client.get('/', data={'name':'allisson'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.request_started.path_qs, '/?name=allisson')
        
            # request with headers
            resp = self.client.get('/', headers={'NAME':'allisson'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.request_started.headers['NAME'], 'allisson')

        def test_post(self):
            # test status code
            resp = self.client.post('/')
            self.assertEqual(resp.status_code, 200)
        
            # test form
            resp = self.client.post('/', data={'name': 'allisson', 'age': 30})
            self.assertEqual(resp.request_started.POST['name'], 'allisson')
            self.assertEqual(resp.request_started.POST['age'], '30')
        
            # request with headers
            resp = self.client.post('/', headers={'NAME':'allisson'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.request_started.headers['NAME'], 'allisson')

        def test_put_delete_options_head(self):
            resp = self.client.put('/')
            self.assertEqual(resp.status_code, 405)

            resp = self.client.delete('/')
            self.assertEqual(resp.status_code, 405)

            resp = self.client.options('/')
            self.assertEqual(resp.status_code, 405)

            resp = self.client.head('/')
            self.assertEqual(resp.status_code, 405)
    
