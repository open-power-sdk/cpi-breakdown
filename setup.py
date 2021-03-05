#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2017,2019 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Rafael Sene <rpsene@br.ibm.com>
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Matheus Castanho <mscastanho@ibm.com>
"""

from setuptools import setup, find_packages
try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

with open('README.md') as f:
    README = f.read()

REQUIREMENTS_LIST = parse_requirements('./requirements.txt', session=False)
REQUIREMENTS = [str(required.req) for required in REQUIREMENTS_LIST]

setup(
    name='cpi',
    version='1.0.20210306135653',
    description='Profiles C/C++ applications with the CPI (cycles per \
instruction) breakdown model for POWER8',
    long_description=README,
    author='Rafael Peria de Sene, Roberto Guimarães Dutra de Oliveira, \
Daniel Battaiola Kreling, Diego Fernandez Merjildo',
    author_email='rpsene@br.ibm.com, rdutra@br.ibm.com, \
dbkreling@br.ibm.com, merjildo@br.ibm.com',
    url='https://developer.ibm.com/linuxonpower/sdk/',
    license='Apache Software License 2.0',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/cpi'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License 2.0',
        ],
)
