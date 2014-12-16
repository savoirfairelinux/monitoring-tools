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

URL = 'http://www.quebecrencontres.com/'
XPATH = '//div[@id="top"]/h2[@class="txtlarge"]/text()'

class Plugin(BasePlugin):
    NAME = 'check-quebecrencontrescom'
    VERSION = '0.1'
    DESCRIPTION = 'Checks number of lonely hearts on quebecrencontres.com.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
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
        data = tree.xpath(XPATH)
        if len(data) == 1:
            data = data[0]
            data = data.strip().replace(' ', '')
            results = [x for x in re.split('[^0-9]', data) if x]
            try:
                results = [int(x) for x in results[:2]]
            except Exception as e:
                self.exit(STATES.UNKWOWN, 'Wrong data received: %s' % results)

            p1 = PerfData('members', results[0], min_=0)
            p2 = PerfData('online', results[1], min_=0)
            self.exit(STATES.OK, 'OK - %d members, %d online' % tuple(results), p1, p2)
        
        self.exit(STATES.UNKWOWN, 'Wrong data received: %s [...]' % html[:100])

if __name__ == "__main__":
    Plugin()
