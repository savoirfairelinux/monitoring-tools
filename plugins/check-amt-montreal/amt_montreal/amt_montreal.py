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
import urllib2
import gtfs_realtime_pb2 as gtfs
import warnings

from shinkenplugins.perfdata import PerfData
from shinkenplugins.helpers.argparse import escape_help
from shinkenplugins.helpers.argparse.parsing.bytes import (
    ByteAmountParser,
    adv_byte_unit_to_transformer,
    PercentValue,
)
from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.states import STATES

class CheckAmtMontreal(ShinkenPlugin):
    NAME = 'amt_montreal'
    VERSION = '1.0'
    DESCRIPTION = 'Checks the numbers of warnings reported by the AMT trains in the Montreal area.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'


    def __init__(self):
        super(CheckAmtMontreal, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--url', '-U', required=True, help='the url to fetch data from')
        self.parser.add_argument('--token', '-t', required=True, help='your AMT API access token')



    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckAmtMontreal, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args

    def get_feed(self, url):
        try:
            feed = urllib2.urlopen(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'UNKNOWN - Error while opening url: %s' % str(e))
        if feed.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'UNKNOWN - HTTP error: %d' % feed.getcode())
        return feed.read()

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        # fetches data
        url = args.url + '?token=' + args.token
        data = self.get_feed(url)

        alerts = gtfs.FeedMessage()
        try:
            alerts.ParseFromString(data)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'UNKNOWN - Bad data format or unknown error: %s' % e)

        nb = len(alerts.entity)
        str_plural = 'problems' if nb >= 2 else 'problem'
        message = '%d %s' % (nb, str_plural)

        perfdata = PerfData('problems', nb,
                            warn=int(args.warning),
                            crit=int(args.critical),
                            min_=0)

        if nb < int(args.warning):
            self.exit(STATES.OK, message, perfdata)
        elif nb < int(args.critical):
            self.exit(STATES.WARNING, message, perfdata)
        else:
            self.exit(STATES.CRITICAL, message, perfdata)



############################################################################

Plugin = CheckAmtMontreal

############################################################################

def main():
    plugin = CheckAmtMontreal()
    plugin.execute()


if __name__ == "__main__":
    main()