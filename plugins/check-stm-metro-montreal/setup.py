#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2014, Savoir-faire Linux, Inc.
#
# Authors:
#   Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
#   Grégory Starck <gregory.starck@savoirfairelinux.com>
#
#############################################################################

from __future__ import with_statement

from os import path
from setuptools import setup, find_packages

THIS_DIR = path.abspath(path.dirname(__file__))

ns = {}
with open(path.join(THIS_DIR, 'shinkenplugins', 'plugins',
                    'stm_metro_montreal', 'version.py')) as fh:
    exec(fh.read(), ns, ns)
    VERSION = ns['VERSION']


description = 'Check STM Metro Montreal'
long_description = description

#############################################################################

setup(
    name='shinkenplugins.plugins.stm_metro_montreal',
    author="Grégory Starck",
    author_email="gregory.starck@savoirfairelinux.com",
    long_description=long_description,
    description=description,
    license="GPL3+",
    url="https://github.com/savoirfairelinux/monitoring-tools",
    platforms=['any'],
    version=VERSION,
    packages=find_packages(),
    namespace_packages=[
        'shinkenplugins',
        'shinkenplugins.plugins',
    ],
    install_requires=[
        'shinkenplugins>0.4.0',
        'lxml',
    ],
    extras_require={
        'test': [
            'nose'
        ],
    },
    entry_points="""
    [console_scripts]
    check_stm_metro_montreal = shinkenplugins.plugins.stm_metro_montreal:main
    """,
)
