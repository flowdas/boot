# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

setup_requires = [
    ]

install_requires = [
    ]

tests_require = [
    'nose==1.3.0',
    'coverage==3.7',
    ]

if sys.version_info < (2, 7):
    tests_require.append('unittest2==0.5.1')

dependency_links = [
    ]

setup(
    name='Flowdas-Boot',
    version='1.0a1',
    description='Flowdas Boot',
    author='Flowdas',
    author_email='prospero@flowdas.com',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        },
    dependency_links=dependency_links,
    test_suite='nose.collector',
    scripts=[],
    entry_points={
        'console_scripts': [
            ],
        },
    )
