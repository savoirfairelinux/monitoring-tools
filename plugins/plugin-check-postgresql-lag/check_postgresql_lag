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

import psycopg2
import sys
import re
from shinkenplugins import BasePlugin, PerfData, STATES
class Plugin(BasePlugin):
    NAME = 'check-postgresql-lag'
    VERSION = '0.1'
    DESCRIPTION = 'check postgresql streaming latency'
    AUTHOR = 'vdnguyen'
    EMAIL = 'vanduc.nguyen@savoirfairelinux.com'

    ARGS = [('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('u', 'url', 'the url to fetch data from', True),
            ('w', 'warning', ('Limit to result in a warning state: MB, '
                              'by default is 2 times wal_segment'), True),
            ('c', 'critical', ('Limit to result in a critical state: MB, '
                               'by default is 4 times wal_segment'), True),
            ('H', 'host', 'Name of host', True),
            ('p', 'port', 'Port of postgresql', True),
            ('d', 'db', 'Name of database', True),
            ('u', 'user', 'Name of user', True),
            ('P', 'password', 'Password of the user', True), ]

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.

        # all required args
        if "host" not in args:
            self.exit(STATES.UNKNOWN, "The host argument is missing")
        if "port" not in args:
            self.exit(STATES.UNKNOWN, "The port argument is missing")
        if "user" not in args:
            self.exit(STATES.UNKNOWN, "The user argument is missing")
        if "password" not in args:
            self.exit(STATES.UNKNOWN, "The password argument is missing")
        if "db" not in args:
            self.exit(STATES.UNKNOWN, "The name of database argument is missing")

        # non required args
        if "warning" in args and "critical" not in args:
            self.exit(STATES.UNKNOWN, "The critical argument is missing")
        if "critical" in args and "warning" not in args:
            self.exit(STATES.UNKNOWN, "The warning argument is missing")
        return True, None

    @staticmethod
    def xlog_to_bytes(xlog):
        # This function takes xlog number like "0/C6321D98" and convert to int
        logid, offset = xlog.split('/')
        return (int('ffffffff', 16) * int(logid, 16)) + int(offset, 16)

    def run(self, args):
        # get all data from args
        db = args.get("db")
        user = args.get("user")
        password = args.get("password")
        host = args.get("host")
        port = args.get("port")
        # create connection
        connection = None
        try:
            connection = psycopg2.connect(database=db,
                                          user=user,
                                          password=password,
                                          host=host,
                                          port=port)
            cursor = connection.cursor()
            # use SELECT sql command to get list of data
            cursor.execute("SELECT * from pg_stat_replication;")
            # fetch all data in list
            data_list = cursor.fetchone()
            # create variables we need to calculate lag
            sent_location = Plugin.xlog_to_bytes(data_list[9])
            replay_location = Plugin.xlog_to_bytes(data_list[12])
            # calculate lag in bytes and convert to MB
            lag = (sent_location - replay_location) / (1024.0 ** 2)
            # use sql command to get wal_segment
            cursor.execute("SHOW wal_segment_size")
            # fetch wal_segment in variable
            wal_segment = cursor.fetchone()
            # get int in wal_segment
            wal_segment_int = int(re.match(r'\d+', wal_segment[0]).group())
            # get string in wal_segment
            wal_segment_unit = ''.join([i for i in wal_segment[0] if not i.isdigit()])
            # handle warning et critical
            if args.get("warning"):
                warning = int(args.get("warning"))
                critical = int(args.get("critical"))
            else:
                warning = wal_segment_int * 2
                critical = wal_segment_int * 4

        except psycopg2.DatabaseError:
            print "Error %s"
            sys.exit(1)
        finally:
            if connection:
                connection.close()

        if lag > critical:
            message = "CRITICAL: there's %0.2f %s of latency" % (lag, wal_segment_unit)
            code = STATES.CRITICAL
        elif lag > warning:
            message = "WARNING: there's %0.2f %s of latency" % (lag, wal_segment_unit)
            code = STATES.WARNING
        else:
            message = "OK: there's %0.2f %s of latency" % (lag, wal_segment_unit)
            code = STATES.OK
        # convert lag to float with 2 decimal places
        lag = "%0.2f" % (lag)
        p1 = PerfData('lag', lag, unit=wal_segment_unit, warn=warning, crit=critical, min_=0)

        self.exit(code, message, p1)

if __name__ == "__main__":
    Plugin()
