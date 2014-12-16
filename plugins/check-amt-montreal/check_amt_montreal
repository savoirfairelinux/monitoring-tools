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
# Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>

from shinkenplugins import BasePlugin, PerfData, STATES
import urllib2
import gtfs_realtime_pb2 as gtfs


class Plugin(BasePlugin):
    NAME = 'check-amt-montreal'
    VERSION = '0.1'
    DESCRIPTION = 'Checks the numbers of warnings reported by the AMT trains in the Montreal area.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('U', 'url', 'the url to fetch data from', True),
            ('t', 'token', 'your AMT API access token', True),
            ('w', 'warning', 'warning level (number of alerts)', True),
            ('c', 'critical', 'critical level (number of alerts)', True),
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get('help') and not args.get('version'):
            for arg in ['url', 'token', 'warning', 'critical']:
                if not arg in args.keys():
                    return False, 'arg %s must be present' % arg
        return True, None
    
    def get_feed(self, url):
        try:
            feed = urllib2.urlopen(url)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'UNKNOWN - Error while opening url: %s' % str(e))
        if feed.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'UNKNOWN - HTTP error: %d' % feed.getcode())
        return feed.read()

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        
        # fetches data
        url = args['url'] + '?token=' + args['token']
        data = self.get_feed(url)

        alerts = gtfs.FeedMessage()
        try:
            alerts.ParseFromString(data)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'UNKNOWN - Bad data format or unknown error: %s' % e)

        nb = len(alerts.entity)
        str_plural = 'problems' if nb >= 2 else 'problem'
        message = '%d %s' % (nb, str_plural)

        perfdata = PerfData('problems', nb,
                            warn=int(args['warning']),
                            crit=int(args['warning']),
                            min_=0)
        
        if nb < int(args['warning']):
            self.exit(STATES.OK, 'OK - ' + message, perfdata)
        elif nb < int(args['critical']):
            self.exit(STATES.WARNING, 'WARNING - ' + message, perfdata)
        else:
            self.exit(STATES.CRITICAL, 'CRITICAL - ' + message, perfdata)

if __name__ == "__main__":
    Plugin()
