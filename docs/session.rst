Session
============

You need to set SECRET_KEY in your config to use the session:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from gunstar.app import Application


    class ConfigSettings(object):
    
        SECRET_KEY = 'my-secret-key'


    routes = (
        ('/', 'handlers.IndexHandler', 'index'),
    )


    myapp = Application(routes=routes, config=ConfigSettings)
    

If you want to create a good secret key, follow this snippet:

.. code-block:: python
    
    # snippet from http://flask.pocoo.org/docs/quickstart/#sessions
    >>> import os
    >>> os.urandom(24)
    '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


