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
import lxml.html

from shinkenplugins.perfdata import PerfData
from shinkenplugins.helpers.argparse import escape_help
from shinkenplugins.helpers.argparse.parsing.bytes import (
    ByteAmountParser,
    adv_byte_unit_to_transformer,
    PercentValue,
)
from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.states import STATES

class CheckEmergencyRoomsQuebec(ShinkenPlugin):
    NAME = 'emergency_rooms_quebec'
    VERSION = '1.0'
    DESCRIPTION = ('Checks the occupation of stretchers in various hospitals in Quebec.\n'
                   'To find pre-defined hospitals configuration, please check\n'
                   'https://github.com/matthieucan/quebec-monitoring/blob/master/scripts/hospitals.py')
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'


    def __init__(self):
        super(CheckEmergencyRoomsQuebec, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--url', '-U', required=True, help='The url to check.')
        self.parser.add_argument('-f', '--functional_stretchers', help='XPATH to the functional stretchers value', required=True)
        self.parser.add_argument('-o', '--occupied_stretchers', help='XPATH to the occupied stretchers value', required=True)


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckEmergencyRoomsQuebec, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args


    def get_html(self, url):
        opener = urllib2.build_opener()
        # agence.santemontreal.qc.ca seems to prohibit access (403) to "custom" http agents (
        # like urllib2 one) ; by forcing User-agent we workaround the problem:
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            html = opener.open(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error while opening url: %s' % str(e))
        if html.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'HTTP error: %d' % html.getcode())
        return html.read()

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        html = self.get_html(args.url)
        tree = lxml.html.fromstring(html)
        data1 = tree.xpath(args.functional_stretchers)
        data2 = tree.xpath(args.occupied_stretchers)

        if len(data1) == len(data2) == 1:
            try:
                data1 = int(data1[0].strip())
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Not integer (functional stretchers): %s' % data1)
            try:
                data2 = int(data2[0].strip())
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Not integer (occupied stretchers): %s' % data2)

            result = 100 * data2 / data1
            p1 = PerfData('functional_stretchers', data1, min_=0)
            p2 = PerfData('occupied_stretchers', data2, min_=0)
            p3 = PerfData('occupation', result, warn=args.warning, crit=args.critical, min_=0, max_=100)

            if result < int(args.warning):
                self.exit(STATES.OK, '%d%%' % result, p1, p2, p3)
            elif result < int(args.critical):
                self.exit(STATES.WARNING, '%d%%' % result, p1, p2, p3)
            else:
                self.exit(STATES.CRITICAL, '%d%%' % result, p1, p2, p3)

        self.exit(STATES.UNKNOWN, 'Wrong data extracted: %s - %s' % (data1, data2))



############################################################################

Plugin = CheckEmergencyRoomsQuebec

############################################################################

def main():
    plugin = CheckEmergencyRoomsQuebec()
    plugin.execute()


if __name__ == "__main__":
    main()