# -*- coding: utf-8 -*-
from setuptools import setup
import sys


requires = [
    'WebOb>=1.2.3',
    'blinker>=1.3',
    'Jinja2>=2.7.1',
    'six>=1.3.0',
]
if sys.version_info < (2, 7):
    requires.append('importlib>=1.0.2')


setup(
    name='Gunstar',
    version='0.1',
    author='Allisson Azevedo',
    author_email='allisson@gmail.com',
    packages=['gunstar'],
    license='MIT',
    description='Another python web framework.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires
)
