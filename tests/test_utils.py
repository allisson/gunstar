# -*- coding: utf-8 -*-
import unittest
from gunstar.utils import import_from_string


class UtilsTestCase(unittest.TestCase):

    def test_import_from_string(self):
        import gunstar
        from tests.resources import config_settings
        self.assertEqual(
            import_from_string('gunstar.http.Request'),
            gunstar.http.Request
        )
        self.assertEqual(
            import_from_string('gunstar.http.Response'),
            gunstar.http.Response
        )
        self.assertEqual(
            import_from_string('gunstar.http'),
            gunstar.http
        )
        self.assertEqual(
            import_from_string('tests.resources.config_settings'),
            config_settings
        )
        self.assertEqual(
            import_from_string('gunstar'),
            gunstar
        )
