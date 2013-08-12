# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='Gunstar',
    version='0.1',
    author='Allisson Azevedo',
    author_email='allisson@gmail.com',
    packages=['gunstar'],
    license='LICENSE',
    description='Another python web framework.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'WebOb>=1.2.3',
        'Routes>=1.13',
        'blinker>=1.3',
        'Jinja2>=2.7.1',
    ]
)
