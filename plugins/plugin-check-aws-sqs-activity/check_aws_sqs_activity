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

from shinkenplugins import BasePlugin, PerfData, STATES
import boto
import datetime


class Plugin(BasePlugin):
    NAME = 'check-aws-sqs-activity'
    VERSION = '0.1'
    DESCRIPTION = 'Checks the activity of AWS simple queue service.'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre@alexandreviau.net'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('k', 'acceskey', 'AWS Acces Key ID (optional)', True),
            ('s', 'secretkey', 'AWS Secret Key ID (optional)', True),
            ('q', 'queue', 'Name of the queue', True),
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get('queue'):
            return False, 'you must specify a queue to monitor'

        return True, None
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        acceskey = args.get('acceskey')
        secretkey = args.get('secretkey')

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

if __name__ == "__main__":
    Plugin()
