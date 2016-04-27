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

class CheckCountRabbitmqQueues(ShinkenPlugin):
    NAME = 'count_rabbitmq_queues'
    VERSION = '1.0'
    DESCRIPTION = 'check the number of queue on a rabbitmq server'
    AUTHOR = 'Flavien Peyre'
    EMAIL = 'flavien.peyre@savoirfairelinux.net'


    def __init__(self):
        super(CheckCountRabbitmqQueues, self).__init__()
        self.add_warning_critical(
            {'help': "The maximum time to receive the message in the output queue after which "
                     "we consider a WARNING result.",
             'default': None},
            {'help': "The maximum time to receive the message in the output queue after which "
                     "we consider a CRITICAL result.",
             'default': None},)
        self.parser.add_argument('--url', '-u', required=True, help='The url to check.')
        self.parser.add_argument('-f', '--perfdata', action='store_true',
            help='option to show perfdata'),


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckCountRabbitmqQueues, self).parse_args(args)
        return args


    def run(self, args):
        """ Main Plugin function """
        count_of_queue = int(os.system('rabbitmqctl list_queues name |wc -l'))
        p = PerfData('Count of queues', count_of_queue, unit='queues', warn=args.warn, crit=args.critical, min_=0)

        if args.critical and count_of_queue < args.critical:
            self.critical("Critical", p)
        elif args.warning and count_of_queue < args.warning:
            self.warning("Warning", p)
        else:
            self.ok("Everything was perfect", p)



############################################################################

Plugin = CheckCountRabbitmqQueues

############################################################################

def main(argv=None):
    plugin = CheckCountRabbitmqQueues()
    plugin.execute(argv)


if __name__ == "__main__":
    main()