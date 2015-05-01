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
# 2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin
import psutil
from influxdb import InfluxDBClient
import re
import requests
import time


class CheckInfluxdb(ShinkenPlugin):
    NAME = 'influxdb'
    VERSION = '1.0'
    DESCRIPTION = 'check if an influxDB instance is launch and some other metrics ( memory allocated, number of shard,hard drive use)'
    AUTHOR = 'Flavien Peyre'
    EMAIL = 'flavien.peyre@savoirfairelinux.com'

    mode = ['connection-time', 'uptime', 'nb-shards', 'nb-write-total', 'write-since-last', 'nb-read-total',
            'read-since-last', 'ROM-allocate', 'RAM-used', 'ROM-used', 'continuous-query', 'routine-go']

    def __init__(self):
        super(CheckInfluxdb, self).__init__()

        self.add_warning_critical()
        self.parser.add_argument('--mode', '-m', required=False, default='connection-time',
                                 help="choose type of warning/critical : " + ','.join(CheckInfluxdb.mode))
        self.parser.add_argument('--host', '-H', required=False, default='localhost',
                                 help='The host of influxdb server.')
        self.parser.add_argument('--port', '-p', required=False, default='8086', help='The port of influxdb server.')
        self.parser.add_argument('--timeout', '-T', required=False, default='10.0', help='timeout de connection')
        self.parser.add_argument('--user', '-u', required=False, default='root', help='user of the monitoring database')
        self.parser.add_argument('--password', '-P', required=False, default='root',
                                 help='password to access to the monitoring database'),

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckInfluxdb, self).parse_args(args)

        if args.mode not in CheckInfluxdb.mode:
            self.parser.error('choose a mode available')
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        args.port = int(args.port)
        args.timeout = float(args.timeout)

        if args.mode == (CheckInfluxdb.mode[0] or CheckInfluxdb.mode[8] or CheckInfluxdb.mode[9]):
            args.warning = float(args.warning)
            args.critical = float(args.critical)
        else:
            args.warning = int(args.warning)
            args.critical = int(args.critical)

        if args.warning > args.critical:
            self.parser.error('warning can not be higher than critical')
        elif (args.warning or args.critical) < 0.0:
            self.parser.error('warning and critical must be higher than 0')

        return args

    def run(self, args):
        """ Main Plugin function """
        now = time.clock()

        try:
            r = requests.get('http://' + args.host + ':%d/ping' % args.port, timeout=args.timeout)
        except requests.exceptions.Timeout:
            self.exit(3, 'Timeout ')
        except requests.exceptions.ConnectionError:
            self.exit(3, 'Connection Error ')

        if 204 == r.status_code:
            # Connection time
            if args.mode == CheckInfluxdb.mode[0]:
                answer = time.clock() - now
                p = PerfData('ping', answer, unit='ms', warn=args.warning, crit=args.critical, min_=0.0,
                             max_=args.timeout)

            client = InfluxDBClient(args.host, args.port, args.user, args.password)
            list_db = client.get_list_database()
            is_present = False
            for j in range(0, len(list_db) - 1):
                if '_influxdb' in list_db[j].values():
                    is_present = True
                    break

            if is_present:
                # Uptime
                client.switch_database('_influxdb')
                if args.mode == CheckInfluxdb.mode[1]:
                    db = client.query("select uptime from server_diag ")
                    ans = list(db['server_diag'])[len(list(db['server_diag'])) - 1]['uptime']
                    hour = re.split("[a-z]", ans)
                    if len(hour) == 4:
                        answer = 3600 * int(hour[0]) + 60 * int(hour[1]) + float(hour[2])
                    else:
                        answer = 60 * hour[0] + hour[1]
                    p = PerfData('Uptime', answer, unit='s', warn=args.warning, crit=args.critical, min_=0)
                # Number of shards
                db = client.query("select numShards from server_diag")
                nb_shards = list(db['server_diag'])[len(list(db['server_diag'])) - 1]['numShards']
                if args.mode == CheckInfluxdb.mode[2]:
                    answer = nb_shards
                    p = PerfData('Number of shards', answer, warn=args.warning, crit=args.critical, min_=0)
                # nb-write-total
                db = client.query("select value from server_batchWriteRx")
                nb_write_total = list(db['server_batchWriteRx'])[len(list(db['server_batchWriteRx'])) - 1]['value']
                if args.mode == CheckInfluxdb.mode[3]:
                    answer = nb_write_total
                    p = PerfData('Number of write queries', answer, warn=args.warning, crit=args.critical,
                                 min_=0)
                # write-since-last
                if args.mode == CheckInfluxdb.mode[4]:
                    answer = nb_write_total - list(db['server_batchWriteRx'])[len(list(db['server_batchWriteRx'])) - 2][
                        'value']
                    p = PerfData('Number of write since last check', answer, warn=args.warning,
                                 crit=args.critical, min_=0)
                # nb-read-total
                db = client.query("select value from server_queriesExecuted")
                nb_read_total = list(db['server_queriesExecuted'])[len(list(db['server_queriesExecuted'])) - 1]['value']
                if args.mode == CheckInfluxdb.mode[5]:
                    answer = nb_read_total
                    p = PerfData('Number of read queries', nb_read_total, warn=args.warning, crit=args.critical, min_=0)
                # read-since-last
                if args.mode == CheckInfluxdb.mode[6]:
                    answer = nb_read_total - \
                             list(db['server_queriesExecuted'])[len(list(db['server_queriesExecuted'])) - 2]['value']
                    p = PerfData('Number of read queries since last check', answer, warn=args.warning,
                                 crit=args.critical, min_=0)
                # ROM-allocate
                rom_free = psutil.disk_usage('/')[2]
                if args.mode == CheckInfluxdb.mode[7]:
                    answer = nb_shards * 1024 * 1024
                    p = PerfData('ROM allocate', answer, unit='bytes', warn=args.warning, crit=args.critical, min_=0,
                                 max_=answer + rom_free)
                # Ram used
                if args.mode == CheckInfluxdb.mode[8]:
                    db = client.query("select alloc from server_memory")
                    answer = list(db['server_memory'])[len(list(db['server_memory'])) - 1]['alloc']
                    ram_value = psutil.virtual_memory()[0]
                    p = PerfData('RAM used', answer, unit='bytes', warn=args.warning, crit=args.critical, min_=0,
                                 max_=ram_value)
                # Rom Used
                if args.mode == CheckInfluxdb.mode[9]:
                    db = client.query("select value from shard_shardBytes")
                    bytes_per_shard = []
                    for i in range(len(list(db['server_shardBytes'])) - 1 - nb_shards,
                                   len(list(db['shard_shardBytes'])) - 1):
                        bytes_per_shard.append(list(db['shard_shardBytes'])[i]['value'])
                    answer = sum(bytes_per_shard)
                    p = PerfData('ROM used', answer, unit='bytes', warn=args.warning, crit=args.critical, min_=0,
                                 max_=answer + rom_free)
                # continuous-query
                if args.mode == CheckInfluxdb.mode[10]:
                    db = client.query("select cqLastRun from server_diag")
                    ans = list(db['server_diag'])[len(list(db['server_diag'])) - 1]['cqLastRun']
                    hour = re.split("[+,' ',:,-]", ans)
                    s = (int(hour[0]) - 1) * 365 * 24 * 3600 + (int(hour[1]) - 1) * 30.5 * 24 * 3600 + (int(
                        hour[2]) - 1) * 24 * 3600 + int(hour[3]) * 3600 + int(hour[4]) * 60 + int(hour[5])
                    answer = s + int(hour[7]) * 0.0001
                    p = PerfData('Time since last continuous query launch', answer, unit='s', warn=args.warning,
                                 crit=args.critical, min_=0)
                # routine-go
                if args.mode == CheckInfluxdb.mode[11]:
                    db = client.query("select numGoRoutine from server_go")
                    answer = list(db['server_go'])[len(list(db['server_go'])) - 1]['numGoRoutine']
                    p = PerfData('Number of go routine', answer, warn=args.warning, crit=args.critical,
                                 min_=0)

                if answer > args.critical:
                    self.exit(2, args.mode + " > %f" % args.critical, p)
                elif answer > args.warning:
                    self.exit(1, args.mode + " > %f" % args.warning, p)
                else:
                    self.exit(0, "all is good for " + args.mode, p)
            else:
                self.exit(3, "Monitoring database doesn't exist")
        else:
            self.exit(3, "Bad response from Influxdb")


############################################################################

Plugin = CheckInfluxdb

############################################################################


def main(argv=None):
    plugin = CheckInfluxdb()
    plugin.execute(argv)


if __name__ == "__main__":
    main()