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
# Author Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>

import re
import urllib2
import lxml.html

from shinkenplugins import BasePlugin, PerfData, STATES

class Plugin(BasePlugin):
    NAME = 'check-emergency-rooms-quebec'
    VERSION = '0.1'
    DESCRIPTION = ('Checks the occupation of stretchers in various hospitals in Quebec.\n'
                   'To find pre-defined hospitals configuration, please check\n'
                   'https://github.com/matthieucan/quebec-monitoring/blob/master/scripts/hospitals.py')
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('U', 'url', 'the url to fetch data from', True),
            ('w', 'warning', 'Percentage of occupied stretchers to result in a warning state', True),
            ('c', 'critical', 'Percentage of occupied stretchers to result in a critical state', True),
            ('f', 'functional_stretchers', 'XPATH to the functional stretchers value', True),
            ('o', 'occupied_stretchers', 'XPATH to the occupied stretchers value', True),
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        mandatory_args = ['url', 'warning', 'critical', 'functional_stretchers', 'occupied_stretchers']
        if not args.get('help') and not args.get('version'):
            for arg in mandatory_args:
                if not arg in args.keys():
                    return False, 'argument %s is mandatory' % arg
        return True, None

    def get_html(self, url):
        try:
            html = urllib2.urlopen(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error while opening url: %s' % str(e))
        if html.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'HTTP error: %d' % html.getcode())
        return html.read()
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        html = self.get_html(args['url'])
        tree = lxml.html.fromstring(html)
        data1 = tree.xpath(args['functional_stretchers'])
        data2 = tree.xpath(args['occupied_stretchers'])

        if len(data1) == len(data2) == 1:
            try:
                data1 = int(data1[0].strip())
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Not integer (functional stretchers): %s' % data1)
            try:
                data2 = int(data2[0].strip())
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Not integer (occupied stretchers): %s' % data2)
            
            result = 100 * data2 / data1
            p1 = PerfData('functional_stretchers', data1, min_=0)
            p2 = PerfData('occupied_stretchers', data2, min_=0)
            p3 = PerfData('occupation', result, warn=args['warning'], crit=args['critical'], min_=0, max_=100)
            
            if result < int(args['warning']):
                self.exit(STATES.OK, 'OK - %d%%' % result, p1, p2, p3)
            elif result < int(args['critical']):
                self.exit(STATES.WARNING, 'WARNING - %d%%' % result, p1, p2, p3)
            else:
                self.exit(STATES.CRITICAL, 'CRITICAL - %d%%' % result, p1, p2, p3)
        
        self.exit(STATES.UNKNOWN, 'Wrong data extracted: %s - %s' % (data1, data2))

if __name__ == "__main__":
    Plugin()
