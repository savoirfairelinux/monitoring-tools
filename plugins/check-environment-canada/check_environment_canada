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

# Copyright (C) 2014, Savoir-faire Linux, Inc.

import json
import urllib2

from shinkenplugins import BasePlugin, PerfData, STATES

class Plugin(BasePlugin):
    NAME = 'check-environment-canada'
    VERSION = '0.1'
    DESCRIPTION = 'Checks various environment metrics in Canada.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('U', 'url', 'the url to fetch data from', True),
            ('m', 'metric', 'name of the metric to use', True),
            ('w', 'warning', 'Limit to result in a warning state', True),
            ('c', 'critical', 'Limit to result in a critical state', True),
            ]

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get('help') and not args.get('version'):
            for arg in ['url', 'metric']:
                if not arg in args.keys():
                    return False, 'argument %s is mandatory' % arg
        
        if 'warning' in args.keys() and 'critical' not in args.keys():
            self.exit(STATES.UNKWOWN, "Argument 'warning' without argument 'critical'!")
        if 'critical' in args.keys() and 'warning' not in args.keys():
            self.exit(STATES.UNKNOWN, "Argument 'critical' without argument 'warning'!")
        
        return True, None

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
        
        data = self.get_json(args['url'])
        try:
            data = json.loads(data)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error loading json data: %s' % e)

        try:
            result = data['reports'][args['metric']]
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Metric not found: %s' % args['metric'])

        if 'warning' in args.keys():
            # then we're working with numbers
            try:
                result = float(result)
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Error, %s is not a number' % result)

            perfdata = PerfData(args['metric'], result, warn=args['warning'], crit=args['critical'])
            
            if result < float(args['warning']):
                self.exit(STATES.OK, 'OK - %s' % result, perfdata)
            elif result < float(args['critical']):
                self.exit(STATES.WARNING, 'WARNING - %s' % result, perfdata)
            else:
                self.exit(STATES.CRITICAL, 'CRITICAL - %s' % result, perfdata)
        else:
            perfdata = PerfData(args['metric'], result)
            self.exit(STATES.OK, 'OK - %s' % result, perfdata)

if __name__ == "__main__":
    Plugin()