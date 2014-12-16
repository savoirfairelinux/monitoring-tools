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
import datetime


from shinkenplugins import BasePlugin, PerfData, STATES

class Plugin(BasePlugin):
    NAME = 'check-http2'
    VERSION = '0.1'
    DESCRIPTION = "Checks HTTP sites, and doesn't timeout like good'old check_http."
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('U', 'url', 'the url to check', True),
            ('A', 'user-agent', 'User-Agent header', True)
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get('help') and not args.get('version'):
            if not 'url' in args.keys():
                return False, 'the argument --url is mandatory!'
        return True, None
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        url = args['url']

        try:
            request = urllib2.Request(url)
            opener = urllib2.build_opener()
            if args.get('user-agent'):
                request.add_header('User-Agent', args['user-agent'])

            start = datetime.datetime.now()
            code = opener.open(request).getcode()
            end = datetime.datetime.now()

        except Exception as e:
            try:
                code = e.code
                self.exit(STATES.CRITICAL, 'CRITICAL - HTTP %s - %s' % (code, e))

            except Exception:
                self.exit(STATES.UNKNOWN, 'UNKNOWN - %s' % e)

        response_time = end - start
        perfdata = PerfData('response_time',
                            response_time.microseconds / 1000 + response_time.seconds * 1000,
                            unit='ms', min_=0)

        if code < 400:
            self.exit(STATES.OK, 'OK - HTTP %s' % code, perfdata)
        else:
            self.exit(STATES.CRITICAL, 'CRITICAL - HTTP %s' % code, perfdata)

if __name__ == "__main__":
    Plugin()
