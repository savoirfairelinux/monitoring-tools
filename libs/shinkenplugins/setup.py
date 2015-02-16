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

from os.path import join, dirname, abspath
from setuptools import setup, find_packages

# no dependencies yet, might be useful later
# with open('requirements.txt') as f:
#     install_requires = [l for l in f.read().splitlines()
#                         if not l.startswith('#')]

description = 'Shinken plugins wrapper library.'
long_description = ('''\
Library aimed to provide helpers around the creation of Shinken
plugins, and in particular their inputs and outputs. Less code,
less code duplication, less headache.''')

with open(join(dirname(abspath(__file__)), 'shinkenplugins', 'VERSION')) as fh:
    VERSION = fh.readline().strip()

#############################################################################

packages = find_packages()
setup(
    name='shinkenplugins',
    version=VERSION,
    packages=packages,
    namespace_packages=[
        'shinkenplugins',
        'shinkenplugins.plugins'
    ],
    #install_requires=install_requires,
    #zip_safe=False,
    author="Grégory Starck",
    author_email="gregory.starck@savoirfairelinux.com",
    long_description=long_description,
    description=description,
    license="GPL3+",
    url="https://github.com/savoirfairelinux/sfl-shinken-plugins",
    platforms=['any'],
    package_data={
        'shinkenplugins': ['VERSION'],
    },
)
