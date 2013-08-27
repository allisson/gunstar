Routing
============

Just define a tuple with three elements: url, handler and url name.

.. code-block:: python
    
    routes = (
        ('/', 'handlers.IndexHandler', 'index'),
    )


==========================
Working with tokens
==========================

You can set a token in url definition, for example:

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class IndexHandler(RequestHandler):
    
        def get(self, name):
            self.render_template('index.html', name=name)
            
.. code-block:: python

    routes = (
        ('/{name}/', 'handlers.IndexHandler', 'index'),
        # convert to regex r'^/([^/]+)/$'
        # match '/allisson/'
        # match '/@allisson/'
    )

For convinience, you can add a filter to token. 

Example with int filter:

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class PostHandler(RequestHandler):
    
        def get(self, id):
            self.render_template('index.html', id=id)
            
.. code-block:: python

    routes = (
        ('/posts/{id:int}/', 'handlers.PostHandler', 'post_index'),
        # convert to regex r'^/posts/([\d]+)/$'
        # match '/posts/1/'
        # match '/posts/2/'
    )

Example with string filter:

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class SearchHandler(RequestHandler):
    
        def get(self, query):
            self.render_template('index.html', query=query)
            
.. code-block:: python

    routes = (
        ('/search/{query:string}/', 'handlers.SearchHandler', 'search'),
        # convert to regex r'^/search/([\w]+)/$'
        # match '/search/mysearch/'
        # match '/search/my_search/'
    )

Example with slug filter:

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class PostHandler(RequestHandler):
    
        def get(self, title):
            self.render_template('index.html', title=title)
            
.. code-block:: python

    routes = (
        ('/post/{title:slug}/', 'handlers.PostHandler', 'post'),
        # convert to regex r'^/post/([\w-]+)/$'
        # match '/post/my_post/'
        # match '/post/my-post/'
    )

Example with path filter:

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class WikiHandler(RequestHandler):
    
        def get(self, title):
            self.render_template('index.html', wiki=wiki)
            
.. code-block:: python

    routes = (
        ('/wiki/{name:path}/', 'handlers.WikiHandler', 'wiki'),
        # convert to regex r'^/wiki/([^/].*?)/$'
        # match '/wiki/Allisson/Detail/'
        # match '/wiki/Allisson/Detail/Age/'
    )
    
Example with re filter:

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class PostHandler(RequestHandler):
    
        def get(self, title):
            self.render_template('index.html', name=name)
            
.. code-block:: python

    routes = (
        ('/post/{name:re:([\w-@]+)}/', 'handlers.PostHandler', 'post'),
        # convert to regex r'^/post/([\w-@]+)/$'
        # match '/post/@allisson-azevedo/'
        # match '/post/@allisson_azevedo/'
    )

============================
Working with handler import
============================

You can import the handler directly or inform the location

.. code-block:: python

    # file handlers.py
    # -*- coding: utf-8 -*-
    from gunstar.http import RequestHandler


    class PostHandler(RequestHandler):
    
        def get(self, title):
            self.render_template('index.html')
            
.. code-block:: python

    from handlers import PostHandler

    # inform location or import directly.
    routes = (
        ('/post1/{title}/', 'handlers.PostHandler', 'post1'),
        ('/post2/{title}/', PostHandler, 'post2'),
    )


