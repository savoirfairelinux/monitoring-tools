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

# Copyright (C) 2014, vdnguyen <vanduc.nguyen@savoirfairelinux.com>
#               2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import

import os
import os.path
import time
import datetime
import argparse
import warnings

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin

class {{ exec_name_capitalized }}(ShinkenPlugin):
    NAME = '{{ short_name }}'
    VERSION = '1.0'
    DESCRIPTION = '{{ desc }}'
    AUTHOR = '{{ author_name }}'
    EMAIL = '{{ author_email }}'


    def __init__(self):
        super({{ exec_name_capitalized }}, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--url', '-u', required=True, help='The url to check.')
        self.parser.add_argument('-f', '--perfdata', action='store_true',
            help='option to show perfdata'),


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super({{ exec_name_capitalized }}, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args


    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        p1 = PerfData('spam', 42, unit='%', warn=70, crit=90, min_=0, max_=100)
        p2 = PerfData('eggs', 6, unit='%', warn=20, crit=30, min_=0, max_=100)

        self.ok("Everything was perfect", p1, p2)



############################################################################

Plugin = {{ exec_name_capitalized }}

############################################################################

def main(argv=None):
    plugin = {{ exec_name_capitalized }}()
    plugin.execute(argv)


if __name__ == "__main__":
    main()
