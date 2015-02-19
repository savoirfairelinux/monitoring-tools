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

import json
import urllib2

from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES

from shinkenplugins.perfdata import PerfData
from shinkenplugins.helpers.argparse import escape_help
from shinkenplugins.helpers.argparse.parsing.bytes import (
    ByteAmountParser,
    adv_byte_unit_to_transformer,
    PercentValue,
)
from shinkenplugins.plugin import ShinkenPlugin

class CheckEnvironmentCanada(ShinkenPlugin):
    NAME = 'environment_canada'
    VERSION = '1.0'
    DESCRIPTION = 'Checks various environment metrics in Canada.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'


    def __init__(self):
        super(CheckEnvironmentCanada, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--url', '-U', required=True, help='The url to check.')
        self.parser.add_argument('-m', '--metric', help='name of the metric to use', required=True)


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckEnvironmentCanada, self).parse_args(args)
        if args.warning is not None and args.critical is None:
            self.parser.error("Argument 'warning' without argument 'critical'!")
        if args.critical is not None and args.warning is None:
            self.parser.error("Argument 'critical' without argument 'warning'!")
        return args


    def get_json(self, url):
        try:
            data = urllib2.urlopen(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error while opening url: %s' % str(e))
        if data.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'HTTP error: %d' % data.getcode())
        return data.read()


    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        data = self.get_json(args.url)
        try:
            data = json.loads(data)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error loading json data: %s' % e)

        try:
            result = data['reports'][args.metric]
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Metric not found: %s' % args.metric)

        if args.warning is not None:
            # then we're working with numbers
            try:
                result = float(result)
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Error, %s is not a number' % result)

            perfdata = PerfData(args.metric, result, warn=args.warning, crit=args.critical)

            if result < float(args.warning):
                self.exit(STATES.OK, '%s' % result, perfdata)
            elif result < float(args.critical):
                self.exit(STATES.WARNING, '%s' % result, perfdata)
            else:
                self.exit(STATES.CRITICAL, '%s' % result, perfdata)
        else:
            perfdata = PerfData(args.metric, result)
            self.exit(STATES.OK, '%s' % result, perfdata)



############################################################################

Plugin = CheckEnvironmentCanada

############################################################################

def main():
    plugin = CheckEnvironmentCanada()
    plugin.execute()


if __name__ == "__main__":
    main()