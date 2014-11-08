# -*- coding: utf-8 -*-
import unittest

from gunstar.routing import Router, Route
from gunstar.http import RequestHandler


class Handler(RequestHandler):

    def get(self):
        self.response.write('Hello')


routes = (
    ('/', 'views.index', 'index'),
    ('/name/{name}/', 'views.other', 'other'),
)


class RouterTestCase(unittest.TestCase):

    def setUp(self):
        self.router = Router()

    def test_init(self):
        router = Router(routes)

        route = router.find_route('/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))

        route = router.find_route('/name/allisson/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))

        route = router.find_route('/other/url')
        self.assertFalse(route)

    def test_add_route(self):
        self.assertEqual(len(self.router.routes), 0)
        self.router.add_route('/', Handler, 'handler')
        self.assertEqual(len(self.router.routes), 1)
        self.assertTrue(
            isinstance(self.router.routes[0], Route)
        )

    def test_find_route(self):
        self.router.add_route('/', Handler, 'index')
        self.router.add_route('/contact/', Handler, 'contact')
        self.router.add_route('/posts/{slug:slug}/', Handler, 'post_detail')

        route = self.router.find_route('/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))

        route = self.router.find_route('/contact/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))

        route = self.router.find_route('/posts/my-post/')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))

        route = self.router.find_route('/other/url')
        self.assertFalse(route)

    def test_find_route_by_name(self):
        self.router.add_route('/', Handler, 'index')
        self.router.add_route('/contact/', Handler, 'contact')
        self.router.add_route('/posts/{slug:slug}/', Handler, 'post_detail')

        route = self.router.find_route_by_name('index')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        self.assertEqual(route.pattern, '/')

        route = self.router.find_route_by_name('contact')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        self.assertEqual(route.pattern, '/contact/')

        route = self.router.find_route_by_name('post_detail')
        self.assertTrue(route)
        self.assertTrue(isinstance(route, Route))
        self.assertEqual(route.pattern, '/posts/{slug:slug}/')

        route = self.router.find_route_by_name('other_url')
        self.assertFalse(route)


class RouteTestCase(unittest.TestCase):

    def test_init(self):
        route = Route('/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/$'
        )

        route = Route('/{name}/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/([^/]+)/$'
        )

        route = Route('/{name:int}/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/([\d]+)/$'
        )

        route = Route('/{name:string}/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/([\w]+)/$'
        )

        route = Route('/{name:slug}/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/([\w-]+)/$'
        )

        route = Route('/{name:re:([\W]+)}/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/([\W]+)/$'
        )

        route = Route('/{name:path}/', Handler, 'index')
        self.assertEqual(
            route.regex_pattern,
            '^/([^/].*?)/$'
        )

    def test_resolve_func(self):
        route = Route('/', Handler, 'index')
        self.assertEqual(route.resolve_func(), Handler)

        from gunstar.utils import import_object
        route = Route(
            '/crazy/handler/',
            'gunstar.utils.import_object',
            'crazy_handler'
        )
        self.assertEqual(route.resolve_func(), import_object)

    def test_get_args(self):
        route = Route('/', Handler, 'index')
        args = route.get_args('/')
        self.assertFalse(args)

        route = Route('/posts/{slug:slug}/', Handler, 'index')
        args = route.get_args('/posts/my-post/')
        self.assertTrue(args)
        self.assertTrue('my-post' in args)

        route = Route(
            '/posts/{id:int}/author/{name:string}/', Handler, 'index'
        )
        args = route.get_args('/posts/1/author/allisson/')
        self.assertTrue(args)
        self.assertTrue('1' in args)
        self.assertTrue('allisson' in args)

        route = Route('/user/{email:re:([\w@]+)}/', Handler, 'index')
        args = route.get_args('/user/@allisson/')
        self.assertTrue(args)
        self.assertTrue('@allisson' in args)

        route = Route('/wiki/{name:path}/', Handler, 'index')
        args = route.get_args('/wiki/Allisson/Detail/')
        self.assertTrue(args)
        self.assertTrue('Allisson/Detail' in args)

    def test_reverse_route(self):
        route = Route('/', Handler, 'index')
        self.assertEqual(route.reverse_route(), '/')

        route = Route('/posts/{slug:slug}/', Handler, 'index')
        self.assertEqual(
            route.reverse_route('my-post'), '/posts/my-post/')

        route = Route(
            '/posts/{id:int}/author/{name:string}/', Handler, 'index'
        )
        self.assertEqual(
            route.reverse_route(12, 'allisson'), '/posts/12/author/allisson/')

        route = Route('/user/{user:re:([\w@]+)}/', Handler, 'index')
        self.assertEqual(
            route.reverse_route('@allisson'), '/user/@allisson/')

        route = Route('/wiki/{name:path}/', Handler, 'index')
        self.assertEqual(
            route.reverse_route('Allisson/Detail'), '/wiki/Allisson/Detail/')
        self.assertEqual(
            route.reverse_route('Allisson/Detail', 'otherargs'),
            None
        )
