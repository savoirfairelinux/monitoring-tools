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
#               2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import

import ctypes
import requests
import sys
import time
from threading import Thread

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin
from multiprocessing import Process, Queue, Value
from shinkenplugins.states import STATES


class CheckHttpLoad(ShinkenPlugin):
    NAME = 'http_load'
    VERSION = '1.0'
    DESCRIPTION = 'A plugin to check the average response time ' \
                  'of a http service under moderate load'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'

    def __init__(self):
        super(CheckHttpLoad, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('-u', '--url', required=True,
                                 help='The url to check.')
        self.parser.add_argument('-n', '--workers', required=True,
                                 help='Number of workers (processes)')
        self.parser.add_argument('-q', '--queries', required=True,
                                 help='Number of queries (threads) per worker')
        self.parser.add_argument('-m', '--max-fail', required=True,
                                 help='Number of fail tolerated before the '
                                      'state becomes critical')
        self.parser.add_argument('-f', '--perfdata', action='store_true',
                                 help='option to show perfdata')

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckHttpLoad, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        args.critical = float(args.critical)
        args.warning = float(args.warning)

        workers = []
        for i in range(int(args.workers)):
            workers.append(Worker(args.url, int(args.queries)))
            workers[i].start()

        all_done = False
        while not all_done:
            time.sleep(0.1)
            all_done = True
            for worker in workers:
                if not worker.done.value:
                    all_done = False

        resp_time = []
        nb_fail = 0
        for worker in workers:
            while not worker.resp_time.empty():
                resp_time.append(worker.resp_time.get())
                nb_fail += worker.nb_fail.value

        if len(resp_time) != 0:
            total = 0.
            for value in resp_time:
                total += value

            mean_time = total / len(resp_time)
        else:
            mean_time = -1

        message = 'Mean time: %.2f seconds'

        if nb_fail > args.max_fail:
            message = 'Too many requests failed'
        elif mean_time >= args.critical:
            code = STATES.CRITICAL
        elif mean_time >= args.warning:
            code = STATES.WARNING
        elif 0 < mean_time < args.warning:
            code = STATES.OK
        else:
            self.unknown("Exited in a unknown state")

        if args.perfdata:
            perf = PerfData('meantime', mean_time,
                            warn=args.warning,
                            crit=args.critical,
                            min_=min(resp_time),
                            max_=max(resp_time))
            self.exit(code, message % mean_time, perf)

        self.exit(code, message % mean_time)


class Worker(Process):

    def __init__(self, url, nb_queries):
        Process.__init__(self)
        self.resp_time = Queue()
        self.url = url
        self.nb_queries = nb_queries
        self.done = Value(ctypes.c_bool, False)
        self.nb_fail = Value('L', 0)

    def run(self):
        threads = []

        for i in range(self.nb_queries):
            threads.append(QueryThread(self.url))
            threads[i].start()

        all_done = False
        while not all_done:
            time.sleep(0.1)
            all_done = True
            for thread in threads:
                if not thread.done.value:
                    all_done = False

        self.done.value = True

        for thread in threads:
            if thread.success.value:
                self.resp_time.put(thread.resp_time.value)
            else:
                self.nb_fail.value += 1


class QueryThread(Thread):

    def __init__(self, url):
        Thread.__init__(self)
        self.resp_time = Value('f')
        self.url = url
        self.done = Value(ctypes.c_bool, False)
        self.success = Value(ctypes.c_bool, True)

    def run(self):
        beg = time.time()

        try:
            response = requests.get(self.url, verify=False)
        except requests.exceptions.RequestException:
            self.success.value = False
            self.done.value = True
            sys.exit()

        if response.status_code != 200:
            self.success.value = False

        delta = time.time() - beg
        self.resp_time.value = delta
        self.done.value = True


############################################################################

Plugin = CheckHttpLoad

############################################################################


def main(argv=None):
    plugin = CheckHttpLoad()
    plugin.execute(argv)


if __name__ == "__main__":
    main()