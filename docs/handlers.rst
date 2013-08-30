Handlers
============

All handlers must be a subclass of gunstar.http.RequestHandler

.. code-block:: python

    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler
    
    
    class Handler(RequestHandler):
    
        def get(self):
            self.response.write('respond GET method')
        
        def post(self):
            self.response.write('respond POST method')


Subclasses of RequestHandler have:

* RequestHandler.request: Instance of `webob.Request <http://docs.webob.org/en/latest/modules/webob.html#request>`_
* RequestHandler.response: Instance of `webob.Response <http://docs.webob.org/en/latest/modules/webob.html#response>`_
* RequestHandler.session: Instance of `gunstar.session.Session <http://gunstar.readthedocs.org/en/latest/session.html>`_

Example:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class IndexHandler(RequestHandler):
    
        def get(self):
            name = self.request.GET.get('name', 'Stranger')
            self.response.write('Hello, {0}'.format(name))


================
Using templates
================

You need to set TEMPLATE_PATH in your config:

.. code-block:: python
    
    # -*- coding: utf-8 -*-
    from gunstar.app import Application
    from gunstar.http import RequestHandler
    import os


    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


    class ConfigSettings(object):
    
        TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')


    class IndexHandler(RequestHandler):
    
        def get(self):
            self.render_template('index.html', var1='var1', var2='var2')


    routes = (
        ('/', IndexHandler, 'index'),
    )


    app = Application(routes=routes, config=ConfigSettings)


You can add `filters <http://jinja.pocoo.org/docs/api/#custom-filters>`_ and `globals <http://jinja.pocoo.org/docs/api/#the-global-namespace>`_ overriding methods:

.. code-block:: python
    
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler

    
    # filter
    def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
        return value.strftime(format)

    
    # global
    def hello(name):
        return 'Hello {0}'.format(name)
    
    
    class BaseHandler(RequestHandler):
    
        def get_template_globals(self):
            template_globals = super(BaseHandler, self).get_template_globals()
            template_globals['hello'] = hello
            return template_globals
        
        def get_template_filters(self):
            template_filters = super(BaseHandler, self).get_template_filters()
            template_filters['datetimeformat'] = datetimeformat
            return template_filters



================
Using abort
================

The method abort() is used to send a http code to client:


.. code-block:: python

    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class IndexHandler(RequestHandler):
    
        def get(self):
            self.abort(404, message='Not found page.')
            # shortcut for:
            # self.response.status_code = 404
            # self.seponse.write('Not found page.')


================
Using redirect
================

The method redirect() is used to redirect client to another location:


.. code-block:: python

    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class IndexHandler(RequestHandler):
    
        def get(self):
            self.redirect('http://gunstar.readthedocs.org')
            # Move to http://gunstar.readthedocs.org with http code = 302
    
    
    class IndexHandler2(RequestHandler):
    
        def get(self):
            self.redirect('http://gunstar.readthedocs.org', permanent=True)
            # Move to http://gunstar.readthedocs.org with http code = 301
            
    
    class IndexHandler3(RequestHandler):
    
        def get(self):
            self.redirect('http://gunstar.readthedocs.org', status_code=307)
            # Move to http://gunstar.readthedocs.org with http code = 307


====================
Using reverse_route
====================

The method reverse_route() is used to generates a url to the given route name:


.. code-block:: python
    
    # -*- coding: utf-8 -*-
    from gunstar.app import Application
    from gunstar.http import RequestHandler


    class IndexHandler(RequestHandler):

        def get(self):
            post_url = self.reverse_route('post_detail', 'my-post-slug')
            self.redirect(post_url)


    class PostHandler(RequestHandler):

        def get(self, post_slug):
            self.response.write('This is the post {0}'.format(post_slug))


    routes = (
        ('/', IndexHandler, 'index'),
        ('/posts/{post_slug:slug}/', PostHandler, 'post_detail'),
    )


    app = Application(routes=routes)
    
