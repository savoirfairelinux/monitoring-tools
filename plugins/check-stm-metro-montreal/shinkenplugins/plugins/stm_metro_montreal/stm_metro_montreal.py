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
import lxml.html

from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES

URL = 'http://www.stm.info/en/info/service-updates/metro'
STATUS_XPATH = '//div[@id="wrap"]/div[@id="sub-wrap"]//div[contains(@class, "content-services")]//section[contains(@class,"item-line")]/p/text()'
LINES_XPATH = '//div[@id="wrap"]/div[@id="sub-wrap"]//div[contains(@class, "content-services")]//section[contains(@class,"item-line")]/h2/text()'
LINES_COUNT = 4


class STM_Metro_Montreal_Plugin(ShinkenPlugin):

    NAME = 'check-stm-metro-montreal'
    VERSION = '0.1'
    DESCRIPTION = 'Checks the current state of the metro in Montreal.'
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'

    def __init__(self):
        super(Plugin, self).__init__()
        self.add_warning_critical(
                {'help': 'Limit to result in a warning state',
                 'default': 3},
                {'help': 'Limit to result in a critical state',
                 'default': 10},
        )

    def get_html(self):
        try:
            html = urllib2.urlopen(URL)
        except Exception as e:
            self.exit(STATES.UNKNOWN, 'Error while opening url: %s' % str(e))
        if html.getcode() >= 400:
            self.exit(STATES.UNKNOWN, 'HTTP error: %d' % html.getcode())
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
            for i in range(LINES_COUNT):
                if status[i] != u'Normal métro service':
                    problems.append(lines[i].strip())

            if 0 <= len(problems) < args.warning:
                msg = 'OK'
                code = STATES.OK
            elif args.warning <= len(problems) < args.critical:
                msg = 'WARNING'
                code = STATES.WARNING
            else:
                msg = 'CRITICAL'
                code = STATES.CRITICAL
            
            perfdata = PerfData('problems', len(problems), warn=args.warning, crit=args.critical,
                                min_=0, max_=LINES_COUNT)
            
            is_problems = len(problems) > 0
            final_msg = ('%(msg)s - %(problems)d problem%(plural)s %(list)s'
                         % {'msg': msg,
                            'problems': len(problems),
                            'plural': 's' if len(problems) >= 2 else '',
                            'list': ': ' + ', '.join(problems) if is_problems else ''})

            self.exit(code, final_msg, perfdata)

        self.unknown('Wrong data received: %s [...]' % html[:100])


Plugin = STM_Metro_Montreal_Plugin


def main():
    Plugin().execute()


if __name__ == "__main__":
    main()
