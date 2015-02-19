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

import os
from os.path import join, dirname, abspath
from setuptools import setup, find_packages

# no dependencies yet, might be useful later
# with open('requirements.txt') as f:
#     install_requires = [l for l in f.read().splitlines()
#                         if not l.startswith('#')]

description = 'Checks the activity of AWS simple queue service.'
long_description = ('''Checks the activity of AWS simple queue service.''')

#############################################################################

setup(
    name='aws_sqs_activity',
    version="1.0",
    packages=["shinkenplugins.plugins.aws_sqs_activity"],
    #install_requires=install_requires,
    #zip_safe=False,
    author="Alexandre Viau",
    author_email="alexandre@alexandreviau.net",
    long_description=long_description,
    description=description,
    license="GPL3+",
    url="https://github.com/savoirfairelinux/sfl-shinken-plugins",
    platforms=['any'],
    install_requires=["shinkenplugins"],
    package_dir={'shinkenplugins.plugins' : ''},
#   MAYBE LATER: use pkg_ressources
#    entry_points="""
#    [console_scripts]
#    check_aws_sqs_activity = shinkenplugins.plugins.aws_sqs_activity.aws_sqs_activity:main
#
#    """
)