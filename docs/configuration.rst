Configuration
=============

Gunstar configuration is handled by gunstar.config.Config class.

Use uppercase letters for your config keys, see the example below.

.. code-block:: python

    >>> from gunstar.config import Config
    >>> class ConfigObject(object):
    ...     KEY1 = 'key1'
    ...     Key2 = 'key2'
    ...     key3 = 'key3'
    ...
    >>> config = Config()
    >>> config.load_from_object(ConfigObject)
    >>> 'KEY1' in config
    True
    >>> 'Key2' in config
    False
    >>> 'key3' in config
    False
    >>>


==========================
How to load config
==========================

Load from object

.. code-block:: python
    
    from gunstar.config import Config

    class ConfigObject(object):

        KEY1 = 'key1'
        key2 = 'key2'

    config = Config()
    config.load_from_object(ConfigObject)


Load from object in python file

.. code-block:: python
    
    # file settings.py
    class Settings(object):
    
        KEY1 = 'key1'
        key2 = 'key2'


.. code-block:: python
    
    from gunstar.config import Config
    
    config = Config()
    config.load_from_object('settings.Settings')


Load from python file

.. code-block:: python
    
    # file settings.py
        
    KEY1 = 'key1'
    key2 = 'key2'

   
.. code-block:: python
    
    from gunstar.config import Config
    
    config = Config()
    config.load_from_object('settings')
