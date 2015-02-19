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

from setuptools import setup, find_packages

#############################################################################

description = 'A Shinken plugin for ceilometer'
long_description = (''' .. ''')


setup(
    name='shinkenplugins.plugins.ceilometer',
    version="1.2",
    packages=find_packages(),
    author="Grégory Starck",
    author_email="gregory.starck@savoirfairelinux.com",
    long_description=long_description,
    description=description,
    license="GPL3+",
    url="https://github.com/savoirfairelinux/sfl-shinken-plugins",
    platforms=['any'],
    install_requires=[
        'shinkenplugins>0.2',
        'python-ceilometerclient==1.0.10',
        'python-keystoneclient==0.8.0',
    ],
    extras_require={
        'test': [
            'nose'
        ],
    },
    namespace_packages=[
        'shinkenplugins',
        'shinkenplugins.plugins',
    ],
    entry_points="""
    [console_scripts]
    check_ceilometer = shinkenplugins.plugins.ceilometer:main
    """,
)

