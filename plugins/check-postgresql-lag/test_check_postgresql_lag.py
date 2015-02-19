#!/usr/bin/python
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

from check_postgresql_lag import Plugin

from shinkenplugins.test import TestPlugin

class Test(TestPlugin):
    def test_version(self):
        args = ['-v']
        self.execute(Plugin, args, 3,
                     'version ' + Plugin.VERSION)

    def test_help(self):
        args = ['-h']
        self.execute(Plugin, args, 3,
                     'Usage:')

    def test_ok(self):
        args = ["-H", "127.0.0.1", "-p", "5432", "-u", "postgres", "-P", "1234", "-d", "testdb", "-w", "1000000", "-c", "1000000"]
        self.execute(Plugin, args, 0, "OK: there's .* MB of latency")

    def test_warning(self):
        args = ["-H", "127.0.0.1", "-p", "5432", "-u", "postgres", "-P", "1234", "-d", "testdb", "-w", "-1", "-c", "1000000"]
        self.execute(Plugin, args, 1, "WARNING: there's .* MB of latency")

    def test_critical(self):
        args = ["-H", "127.0.0.1", "-p", "5432", "-u", "postgres", "-P", "1234", "-d", "testdb", "-w", "-1", "-c", "-1"]
        self.execute(Plugin, args, 2, "CRITICAL: there's .* MB of latency")

