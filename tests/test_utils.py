# -*- coding: utf-8 -*-
import unittest
from gunstar.utils import import_object


class UtilsTestCase(unittest.TestCase):

    def test_import_object(self):
        import gunstar
        from tests.resources import config_settings
        self.assertEqual(
            import_object('gunstar.http.Request'),
            gunstar.http.Request
        )
        self.assertEqual(
            import_object('gunstar.http.Response'),
            gunstar.http.Response
        )
        self.assertEqual(
            import_object('gunstar.http'),
            gunstar.http
        )
        self.assertEqual(
            import_object('tests.resources.config_settings'),
            config_settings
        )
        self.assertEqual(
            import_object('gunstar'),
            gunstar
        )
        self.assertRaises(
            ImportError, import_object, 'gunstar.missing'
        )
