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

from check_snow_clearance import Plugin

from shinkenplugins import TestPlugin

class Test(TestPlugin):
    def test_version(self):
        args = ['-v']
        self.execute(Plugin, args, 3, 'version ' + Plugin.VERSION)

    def test_help(self):
        args = ['-h']
        self.execute(Plugin, args, 3, 'Usage:')

    def test_ok(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-w", "0", "-c", "0"]
        self.execute(Plugin, args, 0, "OK: .*% in 'Mercier-Hochelaga-Maisonneuve' is clear")

    def test_warning(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-w", "101", "-c", "0"]
        self.execute(Plugin, args, 1, "WARNING: .*% in 'Mercier-Hochelaga-Maisonneuve' is clear")

    def test_critical(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-w", "101", "-c", "101"]
        self.execute(Plugin, args, 2, "CRITICAL: .*% in 'Mercier-Hochelaga-Maisonneuve' is clear")

    def test_invalid_borough(self):
        args = ["-b", "abc", "-w", "101", "-c", "101"]
        self.execute(Plugin, args, 3, "Borough 'abc' unknown")

    def test_missing_warning(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-c", "30"]
        self.execute(Plugin, args, 3, "Warning argument is missing")

    def test_missing_critical(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-w", "70"]
        self.execute(Plugin, args, 3, "Critical argument is missing")

    def test_invalid_warning(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-w", "abc", "-c", "30"]
        self.execute(Plugin, args, 3, "Enter warning argument in integer")

    def test_invalid_critical(self):
        args = ["-b", "Mercier-Hochelaga-Maisonneuve", "-w", "70", "-c", "abc"]
        self.execute(Plugin, args, 3, "Enter critical argument in integer")

    def test_missing_borough_argument(self):
        args = []
        self.execute(Plugin, args, 3, "Borough argument is missing")