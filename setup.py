#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Gonéri Le Bouder
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import setuptools

import dci_lite


setuptools.setup(
    name='dci_lite',
    version=dci_lite.__version__,
    author='Gonéri Le Bouder',
    author_email='goneri@lebouder.net',
    description='An alternative client for the distributed-ci.io',
    url='https://github.com/goneri/dci-lite',
    license='Apache v2.0',
    packages=['dci_lite'],
    install_requires=[
        'python-dateutil',
        'dciclient',
    ],
)
