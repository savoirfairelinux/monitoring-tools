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

# Copyright (C) 2014, Flavien Peyre <flavien.peyre@savoirfairelinux.com>

import unittest

from shinkenplugins.test import TestPlugin

from shinkenplugins.plugins.influxdb import Plugin


class Testinfluxdb(TestPlugin):
    def setUp(self):
        # Make stuff before all tests
        pass

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    # Add your tests here!
    # They should use
    # self.execute(Plugin,
    #              ['your', 'list', 'of', 'arguments'],
    #              expected_return_value,
    #              'regex to check against the output')
    # You can also add debug=True, to get useful information
    # to debug your plugins

    def test_timeout(self):
        args = ["-c 11.0", "-w 10.0", "-T 0.0001"]
        self.execute(Plugin, args, 3, "Timeout")

    def test_no_connection(self):
        args = ["-H bla", "-c 10.0", "-w 5.0"]
        self.execute(Plugin, args, 3, "Connection Error")

    def test_connection_time_warning(self):
        args = ["-w 0.000001", "-c 10.0", "--mode", "connection-time"]
        self.execute(Plugin, args, 1, "connection-time > ")

    def test_connection_time_critical(self):
        args = ["-c 0.000001", "-w 0.000001", "--mode", "connection-time"]
        self.execute(Plugin, args, 2, "connection-time > ")

    def test_connection_time_ok(self):
        args = ["-c 10.0", "-w 5.0", "--mode", "connection-time"]
        self.execute(Plugin, args, 0, "all is good")

    def test_RAM_warning(self):
        args = ["-w 10", "-c 10000000000000000", "--mode", "RAM-used"]
        self.execute(Plugin, args, 1, "RAM-used > ")

    def test_RAM_critical(self):
        args = ["-c 10", "-w 5", "--mode", "RAM-used"]
        self.execute(Plugin, args, 2, "RAM-used > ")

    def test_RAM_ok(self):
        args = ["-c 100000000", "-w 75000000", "--mode", "RAM-used"]
        self.execute(Plugin, args, 0, "RAM-used")

if __name__ == '__main__':
    unittest.main()