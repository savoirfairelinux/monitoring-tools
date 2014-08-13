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

# Copyright (C) 2014, Alexandre Viau <alexandre.viau@savoirfairelinux.com>

from shinkenplugins import BasePlugin, PerfData, STATES
import boto


class Plugin(BasePlugin):
    NAME = 'check-aws-sqs-queue-size'
    VERSION = '0.1'
    DESCRIPTION = 'Checks the size of an AWS sqs queue'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre.viau@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('q', 'queue', 'AWS SQS queue name', True),
            ('k', 'acceskey', 'AWS Acces Key ID (optional)', True),
            ('s', 'secretkey', 'AWS Secret Key ID (optional)', True),
            ('w', 'warning', 'Limit to result in a warning state', True),
            ('c', 'critical', 'Limit to result in a critical state', True),
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if args.get('url') and not args['url'].startswith('http'):
            return False, 'the url must be fetchable through http'

        if not args.get('queue'):
            return False, 'you must specify a queue name'

        return True, None
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        acceskey = args.get('acceskey')
        secretkey = args.get('secretkey')

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
                warn=args.get('warn'),
                crit=args.get('crit'),
                min_=0,
            )
        )

        if queue_size > args.get('critical'):
            self.exit(STATES.CRITICAL, "CRITICAL", *perf_data)
        elif queue_size > args.get('warning'):
            self.exit(STATES.WARNING, "WARNING", *perf_data)
        else:
            self.exit(STATES.OK, "OK", *perf_data)

if __name__ == "__main__":
    Plugin()
