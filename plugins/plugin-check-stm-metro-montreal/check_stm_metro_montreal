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

URL = 'http://www.stm.info/en/info/service-updates/metro'
STATUS_XPATH = '//div[@id="wrap"]/div[@id="sub-wrap"]//div[contains(@class, "content-services")]//section[contains(@class,"item-line")]/p/text()'
LINES_XPATH = '//div[@id="wrap"]/div[@id="sub-wrap"]//div[contains(@class, "content-services")]//section[contains(@class,"item-line")]/h2/text()'
LINES_COUNT = 4

class Plugin(BasePlugin):
    NAME = 'check-stm-metro-montreal'
    VERSION = '0.1'
    DESCRIPTION = 'Checks the current state of the metro in Montreal.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('w', 'warning', 'Limit to result in a warning state', True),
            ('c', 'critical', 'Limit to result in a critical state', True),
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get('help') and not args.get('version'):
            for arg in ('warning', 'critical'):
                if not arg in args.keys():
                    return False, 'argument %s is mandatory' % arg
        return True, None

    def get_html(self):
        try:
            html = urllib2.urlopen(URL)
        except Exception as e:
            self.exit(STATES.UNKWOWN, 'Error while opening url: %s' % str(e))
        if html.getcode() >= 400:
            self.exit(STATES.UNKWOWN, 'HTTP error: %d' % html.getcode())
        return html.read()
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        html = self.get_html()
        tree = lxml.html.fromstring(html)
        status = tree.xpath(STATUS_XPATH)
        lines = tree.xpath(LINES_XPATH)

        if len(status) == len(lines) == LINES_COUNT:
            problems = []
            for i in range(len(lines)):
                if status[i] != u'Normal métro service':
                    problems.append(lines[i].strip())

            if 0 <= len(problems) < int(args['warning']):
                msg = 'OK'
                code = STATES.OK
            elif int(args['warning']) <= len(problems) < int(args['critical']):
                msg = 'WARNING'
                code = STATES.WARNING
            else:
                msg = 'CRITICAL'
                code = STATES.CRITICAL
            
            perfdata = PerfData('problems', len(problems), warn=args['warning'], crit=args['critical'],
                                min_=0, max_=LINES_COUNT)
            
            is_problems = len(problems) > 0
            final_msg = ('%(msg)s - %(problems)d problem%(plural)s %(list)s'
                         % {'msg': msg,
                            'problems': len(problems),
                            'plural': 's' if len(problems) >= 2 else '',
                            'list': ': ' + ', '.join(problems) if is_problems else ''})

            self.exit(code, final_msg, perfdata)

        self.exit(STATES.UNKWOWN, 'Wrong data received: %s [...]' % html[:100])

if __name__ == "__main__":
    Plugin()
