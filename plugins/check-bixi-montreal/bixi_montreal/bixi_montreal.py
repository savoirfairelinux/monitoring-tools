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

# Copyright (C) 2014, Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>

import os
import os.path
import time
import datetime
import argparse
import warnings

import urllib2
from lxml import etree

from shinkenplugins.perfdata import PerfData
from shinkenplugins.helpers.argparse import escape_help
from shinkenplugins.helpers.argparse.parsing.bytes import (
    ByteAmountParser,
    adv_byte_unit_to_transformer,
    PercentValue,
)
from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.states import STATES

class CheckBixiMontreal(ShinkenPlugin):
    NAME = 'bixi_montreal'
    VERSION = '1.0'
    DESCRIPTION = 'Checks empty or full Bixi (public bike service) stations, in Montreal.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'


    def __init__(self):
        super(CheckBixiMontreal, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--url', '-U', required=True, help='The url to check.')


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckBixiMontreal, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args


    def get_xml(self, url):
        try:
            xml = urllib2.urlopen(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error while opening url: %s' % str(e))
        if xml.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'HTTP error: %d' % xml.getcode())
        return xml.read()

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        url = args.url
        xml = self.get_xml(url)
        try:
            tree = etree.fromstring(xml)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Incorrect XML received or parser error: %s' % e)

        empty_stations = full_stations = 0
        total = len(tree)
        for station in tree:
            try:
                nbBikes = int(station.find('nbBikes').text)
                nbEmptyDocks = int(station.find('nbEmptyDocks').text)
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Incorrect XML received or parser error: %s' % e)
            if nbEmptyDocks == 0: # Houston, we have a problem
                empty_stations += 1
            if nbBikes == 0:
                full_stations += 1

        problems = empty_stations + full_stations

        str_pb = 'problems' if problems >= 2 else 'problem'

        p1 = PerfData('empty_stations', empty_stations, max_=total)
        p2 = PerfData('full_stations', full_stations, max_=total)
        # no warning and critic, since the values we have are associated to empty+full

        if problems < int(args.warning):
            self.exit(STATES.OK, '%d %s / %d stations' % (problems, str_pb, total), p1, p2)
        elif problems < int(args.critical):
            self.exit(STATES.WARNING, '%d %s / %d stations' % (problems, str_pb, total), p1, p2)
        else:
            self.exit(STATES.CRITICAL, '%d %s / %d stations' % (problems, str_pb, total), p1, p2)



############################################################################

Plugin = CheckBixiMontreal

############################################################################

def main():
    plugin = CheckBixiMontreal()
    plugin.execute()


if __name__ == "__main__":
    main()