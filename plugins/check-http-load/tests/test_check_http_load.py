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

# Copyright (C) 2014, Frédéric Vachon <frederic.vachon@savoirfairelinux.com>

import unittest
import requests
import requests_mock
import time

from shinkenplugins.test import TestPlugin
from shinkenplugins.plugins.http_load import Plugin


CALL_COUNTER = 0


def delayed_matcher(request):
    response = requests.Response()
    response.status_code = 200
    time.sleep(0.05)

    return response


def delayed_failing_matcher(request):
    global CALL_COUNTER
    response = requests.Response()

    CALL_COUNTER += 1
    if CALL_COUNTER % 2 == 0:
        response.status_code = 200
        time.sleep(0.05)
    else:
        response.status_code = 500

    return response


class Testhttp_load(TestPlugin):
    def setUp(self):
        global CALL_COUNTER
        CALL_COUNTER = 0

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    @requests_mock.mock()
    def test_load_ok(self, m):
        m.add_matcher(delayed_matcher)
        expected = 'OK: Mean time:'
        args = ["-u", "http://somesite",
                "-n", "4", "-q", "4", "-m", "0",
                "-w", "4", "-c", "2"]

        self.execute(Plugin, args, 0, expected)

    @requests_mock.mock()
    def test_load_warning(self, m):
        m.add_matcher(delayed_matcher)
        expected = 'WARNING: Mean time:'
        args = ["-u", "http://somesite",
                "-n", "4", "-q", "4", "-m", "0",
                "-w", "0.04", "-c", "2"]

        self.execute(Plugin, args, 1, expected)

    @requests_mock.mock()
    def test_load_critical(self, m):
        m.add_matcher(delayed_matcher)
        expected = 'CRITICAL: Mean time:'
        args = ["-u", "http://somesite",
                "-n", "4", "-q", "4", "-m", "0",
                "-w", "0.01", "-c", "0.03"]

        self.execute(Plugin, args, 2, expected)

    @requests_mock.mock()
    def test_max_fail(self, m):
        m.add_matcher(delayed_failing_matcher)
        expected1 = 'Too many requests failed'
        expected2 = 'Mean time'
        args1 = ["-u", "http://somesite",
                 "-n", "4", "-q", "4", "-m", "7",
                 "-w", "2", "-c", "4"]

        args2 = ["-u", "http://somesite",
                 "-n", "4", "-q", "4", "-m", "8",
                 "-w", "2", "-c", "4"]

        self.execute(Plugin, args1, 2, expected1)
        self.execute(Plugin, args2, 0, expected2)

    @requests_mock.mock()
    def test_perf_data(self, m):
        m.add_matcher(delayed_matcher)
        expected = r"meantime=[0-9.]*;[0-9.]*;[0-9.]*;[0-9.]*;[0-9.]*"
        args = ["-u", "http://somesite",
                "-n", "4", "-q", "4", "-m", "0",
                "-w", "2", "-c", "4", "-f"]

        self.execute(Plugin, args, 0, expected)

    def test_args(self):
        args1 = ["-n", "4", "-q", "4", "-m", "0",
                "-w", "2", "-c", "4"]
        args2 = ["-u", "http://somesite",
                "-q", "4", "-m", "0",
                "-w", "2", "-c", "4"]
        args3 = ["-u", "http://somesite",
                "-n", "4", "-m", "0",
                "-w", "2", "-c", "4"]
        args4 = ["-u", "http://somesite",
                "-n", "4", "-q", "4",
                "-w", "2", "-c", "4"]
        args5 = ["-u", "http://somesite",
                "-n", "4", "-q", "4", "-m", "0",
                "-c", "4"]
        args6 = ["-u", "http://somesite",
                "-n", "4", "-q", "4", "-m", "0",
                "-w", "2"]
        expected1 = "argument -u/--url is required"
        expected2 = "argument -n/--workers is required"
        expected3 = "argument -q/--queries is required"
        expected4 = "argument -m/--max-fail is required"
        expected5 = "error: --warning and --critical are both required"

        self.execute(Plugin, args1, 3, stderr_pattern=expected1)
        self.execute(Plugin, args2, 3, stderr_pattern=expected2)
        self.execute(Plugin, args3, 3, stderr_pattern=expected3)
        self.execute(Plugin, args4, 3, stderr_pattern=expected4)
        self.execute(Plugin, args5, 3, stderr_pattern=expected5)
        self.execute(Plugin, args6, 3, stderr_pattern=expected5)


if __name__ == '__main__':
    unittest.main()