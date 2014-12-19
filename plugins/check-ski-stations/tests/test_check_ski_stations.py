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

import unittest
import os

from shinkenplugins.test import TestPlugin

from shinkenplugins.plugins.ski_stations import Plugin


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# create sub class for test
def make_mocked_plugin(content_file_path):

    content_file_path = os.path.join(THIS_DIR, content_file_path)

    class MockedPlugin(Plugin):

        @classmethod
        def _get_data(cls):
            with open(content_file_path) as fh:
                return fh.read()

    return MockedPlugin


class Test(TestPlugin):
    def test_version(self):
        args = ['-v']
        self.execute(Plugin, args, 3, 'version ' + Plugin.VERSION)

    def test_help(self):
        args = ['-h']
        self.execute(Plugin, args, 3, 'Usage:')

    # check_ski_stations -r Abitibi
    def test_ok(self):
        args = ["-r", "Abitibi"]
        # make_mocked_plugin get "tests/data/tableauqc2014-conditions.php.html"
        # as argument, this is a static data
        self.execute(make_mocked_plugin("data/tableauqc2014-conditions.php.html"),
                     args, 0, "OK: There's .* on .* stations open in Abitibi")

    # check_ski_stations -r Mauricie
    def test_critical(self):
        args = ["-r", "Mauricie"]
        self.execute(make_mocked_plugin("data/tableauqc2014-conditions.php.html"),
                     args, 2, "CRITICAL: There's 0 on .* stations open in Mauricie")

    def test_case_undetermined(self):
        args = ["-r", "Centre du QC"]
        self.execute(make_mocked_plugin("data/tableauqc2014-conditions.php.html"),
                     args, 3, "OK: There's not information for this region")

    def test_invalid_region(self):
        args = ["-r", "abc"]
        self.execute(make_mocked_plugin("data/tableauqc2014-conditions.php.html"),
                     args, 3, "Region u'abc' is unknown.")

    def test_missing_region_argument(self):
        args = []
        self.execute(make_mocked_plugin("data/tableauqc2014-conditions.php.html"),
                     args, 3, "Region argument is missing")


if __name__ == '__main__':
    unittest.main()
