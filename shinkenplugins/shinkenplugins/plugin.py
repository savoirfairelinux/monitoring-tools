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

# Authors:
#   Grégory Starck <gregory.starck@savoirfairelinux.com>
#   Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#############################################################################

from __future__ import unicode_literals, print_function, absolute_import

#############################################################################

import os
import sys
import warnings

try:
    import argparse
except ImportError:
    if sys.version_info[:2] >= (2, 7):
        raise
    warnings.warn('argparse not provided, using the one packaged within shinkenplugins')
    from . import argparse


#############################################################################

def make_plugin_args_parser(progname):
    parser = argparse.ArgumentParser(progname)
    parser.add_argument('-v', '--version', 'Display version number.')
    parser.add_argument('-w', '--warning', 'Warning threshold.')
    parser.add_argument('-c', '--critical', 'Critical threshold.')
    # tbc ..
    return parser


class ShinkenPlugin(object):
    ''' TBC ..
    '''

    def __init__(self):
        pass

