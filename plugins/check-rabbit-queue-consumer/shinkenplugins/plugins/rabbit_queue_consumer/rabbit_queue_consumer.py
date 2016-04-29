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
import subprocess

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin

class CheckRabbitQueueConsumer(ShinkenPlugin):
    NAME = 'rabbit_queue_consumer'
    VERSION = '1.0'
    DESCRIPTION = 'check the number of consumer on a rabbitMQ queue'
    AUTHOR = 'Flavien Peyre'
    EMAIL = 'flavien.peyre@savoirfairelinux.net'


    def __init__(self):
        super(CheckRabbitQueueConsumer, self).__init__()
        self.add_warning_critical({'help': "The minimal number of consummer on the queue to consider a CRITICAL result.",
             'default': None},
            {'help': "The minimal number of consummer on the queue to consider a WARNING result.",
             'default': None},)
        self.parser.add_argument('-q', '--queue', required=True, help='The rabbit queue to check.')
        self.parser.add_argument('-f', '--perfdata', action='store_true',
            help='option to show perfdata'),


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckRabbitQueueConsumer, self).parse_args(args)
        if not args.queue:
            self.parser.error('--queue required')
        return args


    def run(self, args):
        """ Main Plugin function """
        queue, err = subprocess.Popen("rabbitmqctl list_queues name consumers | grep " + args.queue, stdout=subprocess.PIPE,shell = True).communicate()

        if not queue:
            self.unknown("Queue name %s does not exist" % args.queue)
        else:
            consumer = int(queue.split()[-1])
            p = PerfData('Consumer on the queue', memory, unit='consumers', warn=args.warning, crit=args.critical, min_=0)

        if args.critical and consumer < args.critical:
            self.critical("Critical", p)
        elif args.warning and consumer < args.warning:
            self.warning("Warning", p)
        else:
            self.ok("Everything was perfect", p)



############################################################################

Plugin = CheckRabbitQueueConsumer

############################################################################

def main(argv=None):
    plugin = CheckRabbitQueueConsumer()
    plugin.execute(argv)


if __name__ == "__main__":
    main()