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

import urllib2
from lxml import etree

from shinkenplugins import BasePlugin, PerfData, STATES

class Plugin(BasePlugin):
    NAME = 'check-bixi-montreal'
    VERSION = '0.1'
    DESCRIPTION = 'Checks empty or full Bixi (public bike service) stations, in Montreal.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('U', 'url', 'the url to fetch data from', True),
            ('w', 'warning', 'Limit of problematic stations to result in a warning state', True),
            ('c', 'critical', 'Limit of problematic stations to result in a critical state', True),

            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get('help') and not args.get('version'):
            for arg in ['url', 'warning', 'critical']:
                if arg not in args.keys():
                    return False, 'the argument %s must be present' % arg
        return True, None

    def get_xml(self, url):
        try:
            xml = urllib2.urlopen(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error while opening url: %s' % str(e))
        if xml.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'HTTP error: %d' % xml.getcode())
        return xml.read()
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        url = args['url']
        xml = self.get_xml(url)
        try:
            tree = etree.fromstring(xml)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Incorrect XML received or parser error: %s' % e)
        
        empty_stations = full_stations = 0
        total = len(tree)
        for station in tree:
            try:
                nbBikes = int(station.find('nbBikes').text)
                nbEmptyDocks = int(station.find('nbEmptyDocks').text)
            except Exception as e:
                self.exit(STATES.UNKNOWN, 'Incorrect XML received or parser error: %s' % e)
            if nbEmptyDocks == 0: # Houston, we have a problem
                empty_stations += 1
            if nbBikes == 0:
                full_stations += 1

        problems = empty_stations + full_stations

        str_pb = 'problems' if problems >= 2 else 'problem'

        p1 = PerfData('empty_stations', empty_stations, max_=total)
        p2 = PerfData('full_stations', full_stations, max_=total)
        # no warning and critic, since the values we have are associated to empty+full

        if problems < int(args['warning']):
            self.exit(STATES.OK, 'OK - %d %s / %d stations' % (problems, str_pb, total), p1, p2)
        elif problems < int(args['critical']):
            self.exit(STATES.WARNING, 'WARNING - %d %s / %d stations' % (problems, str_pb, total), p1, p2)
        else:
            self.exit(STATES.CRITICAL, 'CRITICAL - %d %s / %d stations' % (problems, str_pb, total), p1, p2)

if __name__ == "__main__":
    Plugin()
