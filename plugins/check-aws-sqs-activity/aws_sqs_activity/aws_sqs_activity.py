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

class CheckAwsSqsActivity(ShinkenPlugin):
    NAME = 'aws_sqs_activity'
    VERSION = '1.0'
    DESCRIPTION = 'Checks the activity of AWS simple queue service.'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre@alexandreviau.net'


    def __init__(self):
        super(CheckAwsSqsActivity, self).__init__()
        self.parser.add_argument('-k', '--acceskey', help='AWS Acces Key ID (optional)')
        self.parser.add_argument('-s', '--secretkey', help='AWS Secret Key ID (optional)')
        self.parser.add_argument('-q', '--queue', help='Name of the queue', required=True)


    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckAwsSqsActivity, self).parse_args(args)
        return args


    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        acceskey = args.acceskey
        secretkey = args.secretkey

        if acceskey is not None and secretkey is not None:
            cloudwatch = boto.connect_cloudwatch(
                aws_access_key_id=acceskey,
                aws_secret_access_key=secretkey
            )
        else:
            cloudwatch = boto.connect_cloudwatch()

        perf_data = []

        msg_received = cloudwatch.get_metric_statistics(
            metric_name='NumberOfMessagesReceived',
            period=60,
            start_time=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            end_time=datetime.datetime.utcnow(),
            namespace='AWS/SQS',
            unit='Count',
            statistics=['Sum'],
            dimensions={'QueueName': [args.get('queue')]}
        )

        msg_deleted = cloudwatch.get_metric_statistics(
            metric_name='NumberOfMessagesDeleted',
            period=60,
            start_time=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            end_time=datetime.datetime.utcnow(),
            namespace='AWS/SQS',
            unit='Count',
            statistics=['Sum'],
            dimensions={'QueueName': [args.get('queue')]}
        )

        if len(msg_deleted) == 0 or len(msg_received) == 0:
            self.exit(STATES.UNKNOWN, "Could not retrieve any metrics")

        number_msg_received = msg_received[0]['Sum']
        perf_data.append(
            PerfData(
                'NumberOfMessagesReceived',
                number_msg_received,
                min_=0,
            )
        )

        number_msg_deleted = msg_deleted[0]['Sum']
        perf_data.append(
            PerfData(
                'NumberOfMessagesDeleted',
                number_msg_deleted,
                min_=0,
            )
        )

        if number_msg_received > 0 and not number_msg_deleted > 0:
            self.exit(
                STATES.CRITICAL,
                "Queue %s is receiving messages but they are not being deleted" % args.get('queue'),
                *perf_data
            )
        else:
            self.exit(STATES.OK, "OK", *perf_data)



############################################################################

Plugin = CheckAwsSqsActivity

############################################################################

def main():
    plugin = CheckAwsSqsActivity()
    plugin.execute()


if __name__ == "__main__":
    main()