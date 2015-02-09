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
# Author Grégory Starck <gregory.starck@savoirfairelinux.com>

import urllib2
import datetime

############################################################################

from shinkenplugins import PerfData, STATES
from shinkenplugins.plugin import ShinkenPlugin

############################################################################

class CheckHttp2(ShinkenPlugin):

    NAME = 'check-http2'
    VERSION = '0.2'
    DESCRIPTION = "Checks HTTP sites, and doesn't timeout like good'old check_http."
    AUTHOR = 'Matthieu Caneill'
    EMAIL = 'matthieu.caneill@savoirfairelinux.com'

    def __init__(self):
        super(CheckHttp2, self).__init__()
        parser = self.parser
        parser.add_argument('--url', '-U', required=True, help='The url to check.')
        parser.add_argument('--user-agent', '-A', default=str(self))

    def run(self, args):
        try:
            request = urllib2.Request(args.url)
            opener = urllib2.build_opener()
            request.add_header('User-Agent', args.user_agent)
            start = datetime.datetime.now()
            code = opener.open(request).getcode()
            end = datetime.datetime.now()
        except Exception as err:
            try:
                code = err.code
                self.critical('HTTP %s - %s' % (code, err))
            except Exception:
                self.unknown('%s' % err)
        else:
            if code >= 400:
                self.critical('HTTP %s' % code)
            else:
                response_time = end - start
                perfdata = PerfData('response_time',
                            response_time.microseconds / 1000 + response_time.seconds * 1000,
                            unit='ms', min_=0)
                self.ok('HTTP %s' % code, perfdata)

############################################################################

Plugin = CheckHttp2

############################################################################
def main():
    plugin = CheckHttp2()
    plugin.execute()
    

if __name__ == "__main__":
    main()
