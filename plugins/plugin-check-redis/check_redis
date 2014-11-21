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

from shinkenplugins import BasePlugin, PerfData, STATES

import sys
import time
import subprocess
import signal

try:
    import redis
except ImportError, e:
    print e
    sys.exit(STATES.OK)

class Plugin(BasePlugin):
    NAME = 'check-redis'
    VERSION = '0.1'
    DESCRIPTION = 'check redis data base'
    AUTHOR = 'vdnguyen'
    EMAIL = 'vanduc.nguyen@savoirfairelinux.com'
    
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('w', 'warning', 'Limit to result in a warning state', True),
            ('c', 'critical', 'Limit to result in a critical state', True),
            ('u', 'unit', 'The unit for representation: KB, MB, GB by default: KB', True),
            ('p', 'port', 'Port of Redis', True),
            ('a', 'command', "Command to use", True),
            ('H', 'host', "Host's name of Redis", True),
            ('d', 'db', "Data base id", True),
            ]
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        
        if not args.get("host"):
            self.exit(STATES.UNKNOWN, "Host is missing")
        if not args.get("port"):
            self.exit(STATES.UNKNOWN, "Port is missing")
        if not args.get("command"):
            self.exit(STATES.UNKNOWN, "Command is missing")
        if not args.get("warning"):
            self.exit(STATES.UNKNOWN, "Warning is missing")
        if not args.get("critical"):
            self.exit(STATES.UNKNOWN, "Critical is missing")
        if not args.get("db"):
            args["db"] = "0"

        return True, None

    def handler_timeout(self, signum, frame):
        self.exit(STATES.UNKNOWN, "WARNING: Could not connect to Redis")

    def check_connect(self, con, host, port, warning, critical, db):
        signal.signal(signal.SIGALRM, self.handler_timeout)
        signal.alarm(30)

        p = subprocess.Popen(["redis-cli", "info"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err != "":
            code = STATES.UNKNOWN
            message = "WARNING: Could not connect to Redis at host: %s, %d" %(host, port)
        else:
            con.ping()
            message = "OK: connection is good, host: %s, port: %s, database id: %s" % (host, port, str(db))
            code = STATES.OK

        self.exit(code, message)

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

    def run(self, args):

        redis_host = args.get("host")
        redis_port = int(args.get("port"))
        warning = args.get("warning")
        critical = args.get("critical")
        redis_db = args.get("db")

        if args.get("unit"):
            unit = args.get("unit")
        else:
            unit = "KB"

        redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db, socket_timeout=3)

        if args.get("command") == "connect":
            Plugin.check_connect(self, redis_conn, redis_host, redis_port, warning, critical, redis_db)
        elif args.get("command") == "connected_clients":
            Plugin.check_connected_clients(self, redis_conn, redis_host, redis_port, warning, critical)
        elif args.get("command") == "used_memory":
            Plugin.check_used_memory(self, redis_conn, redis_host, redis_port, warning, critical)
        elif args.get("command") == "used_memory_human":
            Plugin.check_used_memory_human(self, redis_conn, redis_host, redis_port, warning, critical, unit)
        elif args.get("command") == "used_memory_rss":
            Plugin.check_used_memory_rss(self, redis_conn, redis_host, redis_port, warning, critical)
        elif args.get("command") == "latency":
            Plugin.check_latency(self, redis_conn, redis_host, redis_port, warning, critical)

if __name__ == "__main__":
    Plugin()
