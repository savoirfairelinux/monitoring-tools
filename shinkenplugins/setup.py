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
# Authors:  Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>


from setuptools import setup, find_packages

# no dependencies yet, might be useful later
# with open('requirements.txt') as f:
#     install_requires = [l for l in f.read().splitlines()
#                         if not l.startswith('#')]

description = 'Shinken plugins wrapper library.'
long_description = ('Library aimed to provide helpers around the creation of Shinken\n'
                    'plugins, and in particular their inputs and outputs. Less code,\n'
                    'less code duplication, less headache. More lolz.')

setup(
    name='shinkenplugins',
    version='0.1.2',
    packages=find_packages(),
    #install_requires=install_requires,
    #zip_safe=False,
    author="Matthieu Caneill",
    author_email="matthieu.caneill@savoirfairelinux.com",
    long_description=long_description,
    description=description,
    license="GPL3+",
    url="https://github.com/savoirfairelinux/sfl-shinken-plugins",
    platforms=['any'],
)
