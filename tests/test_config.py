# -*- coding: utf-8 -*-
import unittest
from gunstar.config import Config


class ConfigObject(object):

    KEY1 = 'key1'
    key2 = 'key2'
    Key3 = 'key3'


class ConfigTestCase(unittest.TestCase):

    def test_load_from_object(self):
        config_object = ConfigObject()
        config = Config()
        config.load_from_object(config_object)
        self.assertTrue('KEY1' in config)
        self.assertFalse('key2' in config)
        self.assertFalse('Key3' in config)

        config = Config()
        config.load_from_object('tests.resources.config_settings.Settings')
        self.assertTrue('KEY1' in config)
        self.assertFalse('key2' in config)
        self.assertFalse('Key3' in config)

        config = Config()
        config.load_from_object('tests.resources.config_settings')
        self.assertTrue('KEY1' in config)
        self.assertFalse('key2' in config)
        self.assertFalse('Key3' in config)
