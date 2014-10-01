#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

description = 'Functions and data manipulation for economics data'
with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = 'economics',
    version = '0.1.2',
    url = 'https://github.com/tryggvib/economics',
    license = 'GPLv3',
    description = description,
    long_description = long_description,
    author = 'Tryggvi Björgvinsson',
    author_email = 'tryggvi.bjorgvinsson@okfn.org',
    install_requires = ['datapackage>=0.4.1'],
    packages = ['economics'],
    package_dir={'economics': 'economics'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
    ],
)
