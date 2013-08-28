Application
============

The heart of Gunstar, a wsgi app.

Example:

.. code-block:: python

    # file app.py
    from gunstar.app import Application

    myapp = Application()


In this case, myapp can run with any wsgi server.

Example with wsgiref (included in python):

.. code-block:: python

    # file run.py
    from app import myapp

    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8080, myapp)
    server.serve_forever()

Example with gunicorn (pip install gunicorn):

.. code-block:: bash

    gunicorn app:myapp -b 127.0.0.1:8080


==========================
Initialize routes
==========================

Method one: pass routes tuple directly to Application class

.. code-block:: python

    from gunstar.app import Application

    routes = (
        ('/', 'handlers.IndexHandler', 'index'),
    )


    myapp = Application(routes=routes)


Method two: calling Application.add_route()

.. code-block:: python

    from gunstar.app import Application

    myapp = Application()
    myapp.add_route('/', 'handlers.IndexHandler', 'index')

==========================
Initialize config
==========================

Method one: pass the config directly to Application class

.. code-block:: python

    from gunstar.app import Application

    class Settings(object):
        KEY1 = 'key1'

    myapp = Application(config=Settings)

Method two: calling Application.load_config()

.. code-block:: python

    from gunstar.app import Application

    class Settings(object):
        KEY1 = 'key1'

    myapp = Application()
    myapp.load_config(Settings)
