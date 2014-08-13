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
import requests

class Plugin(BasePlugin):
    NAME = 'check-json-by-ec2-tags'
    VERSION = '0.1'
    DESCRIPTION = 'Runs check-json on all AWS ec2 instances with a particular tag.'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre.viau@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('t', 'tag', 'The tag to look for', True),
            ('e', 'endpoint', 'The endpoint of the json api.  ex: /local_stats', True),
            ('p', 'port', 'The port of the json api.  ex: /local_stats', True),
            ('a', 'attribute', 'The attribute to look for', True),
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

        if not args.get('tag'):
            return False, 'you must specify a tag'

        if not args.get('endpoint'):
            return False, 'you must specify an endpoint'

        if not args.get('port'):
            return False, 'you must specify a port'

        if not args.get('attribute'):
            return False, 'you must specify an attribute to look for'

        return True, None
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        acceskey = args.get('acceskey')
        secretkey = args.get('secretkey')

        if acceskey is not None and secretkey is not None:
            ec2 = boto.connect_ec2(
                aws_access_key_id=acceskey,
                aws_secret_access_key=secretkey
            )
        else:
            ec2 = boto.connect_ec2()

        callers = ec2.get_all_instances(filters={'tag-value': args.get('tag')})
        ips = [r.instances[0].ip_address for r in callers]

        values = []
        for ip in ips:
            try:
                r = requests.get('http://%s:%s%s' % (
                    ip,
                    args.get('port'),
                    args.get('endpoint')
                ))
                value = int(r.json()[args.get('attribute')])
                values.append(value)
            except requests.exceptions.RequestException, e:
                self.exit(STATES.UNKNOWN, "UNKNOWN - %s" % e, [])

        lowest_value = min(values)
        highest_value = max(values)

        lowest_value_perfdata = PerfData(
            'lowest', lowest_value,
            warn=args.get('warning') or '',
            crit=args.get('critical') or '',
            min_=0,
        )

        highest_value_perfdata = PerfData(
            'highest', highest_value,
            warn=args.get('warning') or '',
            crit=args.get('critical') or '',
            min_=0,
        )

        performance_data = [
            lowest_value_perfdata,
            highest_value_perfdata
        ]

        if args.get('critical') and highest_value > args.get('critical'):
            self.exit(STATES.CRITICAL, "CRITICAL", *performance_data)
        elif args.get('warning') and highest_value > args.get('warning'):
            self.exit(STATES.WARNING, "WARNING", *performance_data)
        else:
            self.exit(STATES.OK, "OK", *performance_data)


if __name__ == "__main__":
    Plugin()
