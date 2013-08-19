# -*- coding: utf-8 -*-
import unittest
from gunstar.routing import Router, Route
from gunstar.http import RequestHandler


class Handler(RequestHandler):

    def get(self):
        self.response.write('Hello')


routes = (
    (r'^$', 'views.index', 'index'),
    (r'^name/([\w:-]+)/$', 'views.other', 'other'),
)


class RouterTestCase(unittest.TestCase):
    
    def setUp(self):
        self.router = Router()

    def test_init(self):
        router = Router(routes)
        
        route = router.find_route('')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        
        route = router.find_route('name/allisson/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))

        route = router.find_route('other/url')
        self.assertFalse(route)
    
    def test_add_route(self):
        self.assertEqual(len(self.router.routes), 0)
        self.router.add_route(r'^$', Handler, 'handler')
        self.assertEqual(len(self.router.routes), 1)
        self.assertTrue(
            isinstance(self.router.routes[0], Route)
        )
        
    def test_find_route(self):
        self.router.add_route(r'^$', Handler, 'index')
        self.router.add_route(r'^contact/$', Handler, 'contact')
        self.router.add_route(r'^posts/(?P<slug>[\w:-]+)/$', Handler, 'post_detail')
        
        route = self.router.find_route('')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        
        route = self.router.find_route('contact/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        
        route = self.router.find_route('posts/my-post/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        
        route = self.router.find_route('other/url')
        self.assertFalse(route)
        

class RouteTestCase(unittest.TestCase):
    
    def test_resolve_func(self):
        route = Route(r'^$', Handler, 'index')
        self.assertEqual(route.resolve_func(), Handler)
        
        from gunstar.utils import import_from_string
        route = Route(
            r'^crazy/handler/$',
            'gunstar.utils.import_from_string', 
            'crazy_handler'
        )
        self.assertEqual(route.resolve_func(), import_from_string)
        
    def test_get_args_kwargs(self):
        route = Route(r'^$', Handler, 'index')
        args, kwargs = route.get_args_kwargs('')
        self.assertFalse(args)
        self.assertFalse(kwargs)
        
        route = Route(r'^posts/(?P<slug>[\w:-]+)/$', Handler, 'index')
        args, kwargs = route.get_args_kwargs('posts/my-post/')
        self.assertFalse(args)
        self.assertTrue(kwargs)
        self.assertTrue('slug' in kwargs)
        
        route = Route(r'^posts/([\w:-]+)/$', Handler, 'index')
        args, kwargs = route.get_args_kwargs('posts/my-post/')
        self.assertTrue(args)
        self.assertTrue('my-post' in args)
        self.assertFalse(kwargs)
