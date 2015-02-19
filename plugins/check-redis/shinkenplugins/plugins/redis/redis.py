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

from __future__ import absolute_import

import sys
import time
import subprocess
import signal


import redis


from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES
from shinkenplugins.plugin import ShinkenPlugin


class CheckRedis(ShinkenPlugin):
    NAME = 'check-redis'
    VERSION = '0.1'
    DESCRIPTION = 'Check Redis database'
    AUTHOR = 'Savoir-faire Linux'
    EMAIL = 'supervision@savoirfairelinux.com'
    

    def __init__(self):
        super(CheckRedis, self).__init__()
        parser = self.parser
        parser.add_argument('--warning', '-w', required=False, help='Limit to result in a warning state')
        parser.add_argument('--critical', '-c', required=False, help='Limit to result in a critical state')
        parser.add_argument('--unit', '-u', required=False, help='The unit for representation: KB, MB, GB by default: KB')
        parser.add_argument('--port', '-p', required=False, help='Port of Redis', default=6379)
        parser.add_argument('--command', '-C', required=True,
                            help="Command to use: connect, connected_clients,"
                                 " used_memory, used_memory_human, "
                                 "used_memory_rss, latency")
        parser.add_argument('--host', '-H', required=True, help="Host's name of Redis")
        parser.add_argument('--db', '-d', required=False, help='Database id', default=0)
    
    def handler_timeout(self, signum, frame):
        self.exit(STATES.UNKNOWN, "WARNING: Could not connect to Redis")

    def check_connect(self, con, host, port, warning, critical, db):
        signal.signal(signal.SIGALRM, self.handler_timeout)
        signal.alarm(30)

        #p = subprocess.Popen(["redis-cli", "info"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = p.communicate()
        try:
            start_time = time.time()
            con.info()
            end_time = time.time()
        except Exception:
            code = STATES.CRITICAL
            message = "Could not connect to Redis at host: %s, %d" %(host, port)
            self.exit(code, message)
        
        connection_time = end_time - start_time
        warning = float(warning)
        critical = float(critical)
        if connection_time > critical:
            code = STATES.CRITICAL
            message = "Connection to Redis seems slow: %0.2f s" % connection_time
        elif connection_time > warning:
            code = STATES.WARNING
            message = "Connection to Redis seems slow: %0.2f s" % connection_time
        else:
            code = STATES.OK
            message = "connection is good: %0.2f s" % connection_time

        p1 = PerfData("connection_time", "%0.2f" % connection_time, unit="s", warn=warning, crit=critical, min_=0)
        self.exit(code, message, p1)

    def check_connected_clients(self, con, host, port, warning, critical):
        result = con.info()
        connected_count = int(result["connected_clients"])

        critical = int(critical)
        warning = int(warning)

        if connected_count > critical:
            message = "CRITICAL: there's %s connected clients" % connected_count
            code = STATES.CRITICAL
        elif connected_count > warning:
            message = "WARNING: there's %s connected clients" % connected_count
            code = STATES.WARNING
        else:
            message = "OK: there's %s connected clients" % connected_count
            code = STATES.OK

        p1 = PerfData("connected_count", connected_count, unit="clients", warn=warning, crit=critical, min_=0)
        self.exit(code, message, p1)

    def check_used_memory(self, con, host, port, warning, critical):
        result = con.info()
        used_memory = float(result["used_memory"])

        critical = float(critical)
        warning = float(warning)

        if used_memory > critical:
            message = "CRITICAL: current used memory is %s B" % used_memory
            code = STATES.CRITICAL
        elif used_memory > warning:
            message = "WARNING: current used memory is %s B" % used_memory
            code = STATES.WARNING
        else:
            message = "OK: current used memory is %s B" % used_memory
            code = STATES.OK

        p1 = PerfData("used_memory", used_memory, unit="B", warn=warning, crit=critical, min_=0)
        self.exit(code, message, p1)

    def check_used_memory_human(self, con, host, port, warning, critical, unit):
        result = con.info()
        used_memory_human = result["used_memory_human"]
        used_memory_human = used_memory_human[:-1]
        used_memory_human = float(used_memory_human)
        warning = float(warning)
        critical = float(critical)

        if unit == "GB":
            used_memory_human = used_memory_human / 1024**2
        elif unit == "MB":
            used_memory_human = used_memory_human / 1024

        if used_memory_human > critical:
            message = "CRITICAL: current used memory is %.2f %s" % (used_memory_human, unit)
            code = STATES.CRITICAL
        elif used_memory_human > warning:
            message = "WARNING: current used memory is %.2f %s" % (used_memory_human, unit)
            code = STATES.WARNING
        else:
            message = "OK: current used memory is %.2f %s" % (used_memory_human, unit)
            code = STATES.OK

        used_memory_human = "%0.2f"%(used_memory_human)
        warning = "%0.2f"%(warning)
        critical = "%0.2f"%(critical)
        p1 = PerfData("used_memory_human", used_memory_human, unit=unit, warn=warning, crit=critical, min_=0)
        self.exit(code, message, p1)

    def check_used_memory_rss(self, con, host, port, warning, critical):
        result = con.info()
        used_memory_rss = float(result["used_memory_rss"])

        critical= float(critical)
        warning= float(warning)

        if used_memory_rss > critical:
            message = "CRITICAL: current used memory rss is %s B" % used_memory_rss
            code = STATES.CRITICAL
        elif used_memory_rss > warning:
            message = "WARNING: current used memory rss is %s B" % used_memory_rss
            code = STATES.WARNING
        else:
            message = "OK: current used memory rss is %s B " % used_memory_rss
            code = STATES.OK

        p1 = PerfData("used_memory_rss", used_memory_rss, unit="B", warn=warning, crit=critical, min_=0)
        self.exit(code, message, p1)

    def check_latency(self, con, host, port, warning, critical):
        st = time.time()
        count = 10000
        for i in range(count):
            con.ping()
        et = time.time()
        total_time = et - st

        total_time=float(total_time)
        critical= float(critical)
        warning= float(warning)

        if total_time > critical:
            total_time="%0.2f"%(float(total_time))
            message = "CRITICAL: ping %d times cost %s seconds" % (count, total_time)
            code = STATES.CRITICAL
        elif total_time > warning:
            total_time="%0.2f"%(float(total_time))
            message = "WARNING: ping %d times cost %s seconds" % (count, total_time)
            code = STATES.WARNING
        else:
            total_time="%0.2f"%(float(total_time))
            message = "OK: ping %d times cost %s seconds" % (count, total_time)
            code = STATES.OK

        warning = "%0.2f"%(warning)
        critical = "%0.2f"%(critical)
        p1 = PerfData("total_time", total_time, unit="s", warn=warning, crit=critical, min_=0)
        self.exit(code, message, p1)

    def run(self, arguments):

        redis_host = arguments.host
        redis_port = int(arguments.port)
        warning = arguments.warning
        critical = arguments.critical
        redis_db = arguments.db
        command = arguments.command

        if arguments.unit:
            unit = arguments.unit
        else:
            unit = "KB"

        redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db, socket_timeout=3)

        if command == "connect":
            Plugin.check_connect(self, redis_conn, redis_host, redis_port, warning, critical, redis_db)
        elif command == "connected_clients":
            Plugin.check_connected_clients(self, redis_conn, redis_host, redis_port, warning, critical)
        elif command == "used_memory":
            Plugin.check_used_memory(self, redis_conn, redis_host, redis_port, warning, critical)
        elif command == "used_memory_human":
            Plugin.check_used_memory_human(self, redis_conn, redis_host, redis_port, warning, critical, unit)
        elif command == "used_memory_rss":
            Plugin.check_used_memory_rss(self, redis_conn, redis_host, redis_port, warning, critical)
        elif command == "latency":
            Plugin.check_latency(self, redis_conn, redis_host, redis_port, warning, critical)

############################################################################

Plugin = CheckRedis

############################################################################

def main(argv=None):
    plugin = CheckRedis()
    plugin.execute(argv)


if __name__ == "__main__":
    main()

