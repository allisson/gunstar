.. gunstar documentation master file, created by
   sphinx-quickstart on Mon Aug 19 20:26:18 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Gunstar: Another Python Framework
===================================
Gunstar is a WSGI micro web framework.

`Github Repo <http://github.com/allisson/gunstar/>`_.

=================
Features
=================

* `Based on WebOb <http://docs.webob.org/en/latest/>`_.
* Simple url routing.
* `Jinja2 templates <http://jinja.pocoo.org/docs/>`_.
* Session interface with signed cookies.
* `Signals with blinker <http://pythonhosted.org/blinker/>`_.
* Unit testing support.
* `Supports Python 2.6, 2.7, 3.3 and PyPy <http://travis-ci.org/allisson/gunstar>`_.


=================
Example
=================
Hello World App::

    # -*- coding: utf-8 -*-
    from gunstar.app import Application
    from gunstar.http import RequestHandler

    class IndexHandler(RequestHandler):
        def get(self):
            self.response.write('Hello World')


    routes = (
        ('/', IndexHandler, 'index_named_url'),
    )


    app = Application(routes=routes)


    if __name__ == '__main__':
        from wsgiref.simple_server import make_server
        server = make_server('127.0.0.1', 8080, app)
        server.serve_forever()

=================
Contents
=================

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   configuration
   routing
   application
   handlers
   session
   signals
   testing


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

