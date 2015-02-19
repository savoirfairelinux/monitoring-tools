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

# Copyright (C) 2014, vdnguyen <vanduc.nguyen@savoirfairelinux.com>


import urllib
import re

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin


class CheckApacheServerStatus(ShinkenPlugin):
    NAME = 'apache_server_status'
    VERSION = '1.0'
    DESCRIPTION = 'Get Apache metrics from mod_status Apache status'
    AUTHOR = 'Savoir-faire Linux'
    EMAIL = 'supervision@savoirfairelinux.com'


    def __init__(self):
        super(CheckApacheServerStatus, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--hostname', '-H', required=True, help='Hostadress')
        self.parser.add_argument('--url', '-u', required=True, help='The url to check.')
        self.parser.add_argument('--ssl', '-S', required=False, action='store_true', help='The url to check.')
        self.parser.add_argument('-f', '--perfdata', action='store_true',
                                 help='option to show perfdata'),


    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        scheme = 'https://' if args.ssl else 'http://'

        url = scheme + args.hostname + "/" + args.url + "?auto"
    
        try:
            filehandle = urllib.urlopen(url)
        except Exception as err:
            self.unknown("Unexpected error: %s" % err)

        metrics = {"Total Accesses:(.*)": ("total_acc", "accesses"),
                   "Total kBytes:(.*)": ("total_Kb", "Kb"),
                   "CPULoad:(.*)": ("cpu_load", ""),
                   "Uptime:(.*)": ("uptime", "s"),
                   "ReqPerSec:(.*)": ("req_per_sec", "req_per_sec"),
                   "BytesPerSec:(.*)": ("bytes_per_sec", "bytes_per_sec"),
                   "BytesPerReq:(.*)": ("bytes_per_req", "bytes_per_req"),
                   "BusyWorkers:(.*)": ("busy_workers", "workers"),
                   "IdleWorkers:(.*)": ("idle_workers", "workers"),
                   }

        results = {}
        perfdatas = []
        for line in filehandle.readlines():
            for metric, metric_info in metrics.items():
                name, unit = metric_info
                match = re.match(metric, line)
                if match:
                    value = float(match.group(1).strip())
                    results[name] = value
                    if args.perfdata:
                        perfdatas.append(PerfData(name, value, unit=unit, min_=0))
                    
        if results == {}:
            message = "No data found on %s. Please check you apache configuration"
            self.unknown("Server seems not available (%s)" % message)

        message = " # ".join([ "%s: %0.2f" % (n, v) for n, v in results.items()])
        self.ok(message, *perfdatas)



############################################################################

Plugin = CheckApacheServerStatus

############################################################################

def main(argv=None):
    plugin = CheckApacheServerStatus()
    plugin.execute(argv)


if __name__ == "__main__":
    main()
