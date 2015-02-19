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

# Copyright (C) 2014, Alexandre Viau <alexandre@alexandreviau.net>

import os
import os.path
import time
import datetime
import boto
import argparse
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

class CheckAwsSqsQueueSize(ShinkenPlugin):
    NAME = 'aws_sqs_queue_size'
    VERSION = '1.0'
    DESCRIPTION = 'Checks the size of an AWS sqs queue'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre@alexandreviau.net'


    def __init__(self):
        super(CheckAwsSqsQueueSize, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--url', '-u', required=True, help='The url to check.')
        self.parser.add_argument('-q', '--queue', help='AWS SQS queue name', required=True)
        self.parser.add_argument('-k', '--acceskey', help='AWS Acces Key ID (optional)')
        self.parser.add_argument('-s', '--secretkey', help='AWS Secret Key ID (optional)')



    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckAwsSqsQueueSize, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')

        if args.url is not None and not args.url.startswith('http'):
            self.parser.error('the url must be fetchable through http')

        return args


    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        acceskey = args.acceskey
        secretkey = args.secretkey

        if acceskey is not None and secretkey is not None:
            sqs = boto.connect_sqs(
                aws_access_key_id=acceskey,
                aws_secret_access_key=secretkey
            )
        else:
            sqs = boto.connect_sqs()

        queue = sqs.get_all_queues(prefix=args.get('queue'))[0]
        if queue is None:
            self.exit(STATES.UNKNOWN, "Could not find queue")

        queue_size = queue.count()

        perf_data = []
        perf_data.append(
            PerfData(
                'QueueLenght',
                queue_size,
                warn=args.warning,
                crit=args.critical,
                min_=0,
            )
        )

        if queue_size > args.critical:
            self.exit(STATES.CRITICAL, "CRITICAL", *perf_data)
        elif queue_size > args.warning:
            self.exit(STATES.WARNING, "WARNING", *perf_data)
        else:
            self.exit(STATES.OK, "OK", *perf_data)



############################################################################

Plugin = CheckAwsSqsQueueSize

############################################################################

def main():
    plugin = CheckAwsSqsQueueSize()
    plugin.execute()


if __name__ == "__main__":
    main()