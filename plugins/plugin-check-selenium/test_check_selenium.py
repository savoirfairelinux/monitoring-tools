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

# Copyright (C) 2014, Thibault Cohen <thibault.cohen@savoirfairelinux.com>

from check_selenium import Plugin

from shinkenplugins import TestPlugin

class Test(TestPlugin):
    def test_version(self):
        args = ['-v']
        self.execute(Plugin, args, 3,
                     'version ' + Plugin.VERSION)

    def test_help(self):
        args = ['-h']
        self.execute(Plugin, args, 3,
                     'Usage:')

    # Add your tests here!
    # They should use
    # self.execute(Plugin,
    #              ['your', 'list', 'of', 'arguments'],
    #              expected_return_value,
    #              'regex to check against the output')
    # You can also add debug=True, to get useful information
    # to debug your plugins