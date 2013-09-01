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


==============
Login Example
==============

.. code-block:: python

    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class LoginHandler(RequestHandler):

        def get(self):
            self.render_template('login.html')

        def post(self):
            username = self.request.POST.get('username', None)
            password = self.request.POST.get('password', None)
            user = your_code_to_get_user_by_username_and_password(username, password)
            if user:
                self.session.set('user_id', user.id)
                self.session.save()
                self.redirect('/')
            else:
                error = 'Invalid login'
                self.render_template('login.html', error=error)


    class LogoutHandler(RequestHandler):

        def get(self):
            # if you want to remove all keys in the session:
            # self.session.clear()
            self.session.delete('user_id')
            self.session.save()
            self.redirect('/login/')


    class IndexHandler(RequestHandler):

        def get(self):
            user_id = self.session.get('user_id', None)
            if not user_id:
                self.redirect('/login/')
            user = your_code_to_get_user_by_user_id(user_id)
            self.render_template('index.html', user=user)

