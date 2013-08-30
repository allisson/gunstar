# -*- coding: utf-8 -*-
from setuptools import setup
import sys
import gunstar

version = gunstar.__version__

testing_extras = ['nose', 'coverage']

requires = [
    'WebOb>=1.2.3',
    'blinker>=1.3',
    'Jinja2>=2.7.1',
    'six>=1.3.0',
    'itsdangerous>=0.23',
]
if sys.version_info < (2, 7):
    requires.append('importlib>=1.0.2')


setup(
    name='gunstar',
    version=version,
    author='Allisson Azevedo',
    author_email='allisson@gmail.com',
    packages=['gunstar'],
    license='MIT',
    description='Another python web framework.',
    long_description=open('docs/index.rst').read(),
    url='http://github.com/allisson/gunstar',
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require = {
        'testing': testing_extras,
    },
)
