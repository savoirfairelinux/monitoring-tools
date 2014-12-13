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

import shutil
import os

from shinkenplugins import TestPlugin

from check_linux_bandwidth import Plugin

class Test(TestPlugin):
    def setUp(self):
        if os.path.exists("/tmp/check_linux_bandwith"):
            shutil.rmtree("/tmp/check_linux_bandwith")
        if os.path.exists("/tmp/lo.txt"):
            os.remove("/tmp/lo.txt")

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 3,
                     "version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 3,
                     "Usage:")

    # Add your tests here!
    # They should use
    # self.execute(Plugin,
    #              ['your', 'list', 'of', 'arguments'],
    #              expected_return_value,
    #              'regex to check against the output')
    # You can also add debug=True, to get useful information
    # to debug your plugins

    # check_linux_bandwith_usage -i lo -W 50 -C 90 -d 10 -l 500
    def test_warning_percent_ok(self):
        args = ["-i", "lo", "-W", "1000000", "-C", "1000000", "-d", "5", "-l", "1000000"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_warning(self):
        args = ["-i", "lo", "-W", "0", "-C", "1000000", "-d", "5", "-l", "1000000"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_critical(self):
        args = ["-i", "lo", "-W", "0", "-C", "0", "-d", "5", "-l", "1000000"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*% (.*/1000000.00GB)")

    # check_linux_bandwith_usage -i lo -W 50 -C 90 -d 10 -l 500 -f

    def test_warning_percent_perf_ok(self):
        args = ["-i", "lo", "-W", "1000000", "-C", "1000000", "-d", "5", "-l", "1000000", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_perf_warning(self):
        args = ["-i", "lo", "-W", "0", "-C", "1000000", "-d", "5", "-l", "1000000", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_perf_critical(self):
        args = ["-i", "lo", "-W", "0", "-C", "0", "-d", "5", "-l", "1000000", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*% (.*/1000000.00GB)")

     # check_linux_bandwith_usage -i lo -w 50 -c 100 -d 10 -l 500 -f

    def test_warning_gb_limit_perf_ok(self):
        args = ["-i", "lo", "-w", "1000000", "-c", "1000000", "-d", "5", "-l", "1000000", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_gb_limit_perf_warning(self):
        args = ["-i", "lo", "-w", "0", "-c", "1000000", "-d", "5", "-l", "1000000", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_gb_limit_perf_critical(self):
        args = ["-i", "lo", "-w", "0", "-c", "0", "-d", "5", "-l", "1000000", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*% (.*/1000000.00GB)")

     # check_linux_bandwith_usage -i lo -w 50 -c 90 -d 5
    def test_warning_gb_ok(self):
        args = ["-i", "lo", "-w", "1000000", "-c", "1000000", "-d", "5"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*GB")

    def test_warning_gb_warning(self):
        args = ["-i", "lo", "-w", "0", "-c", "1000000", "-d", "5"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*GB")

    def test_warning_gb_critical(self):
        args = ["-i", "lo", "-w", "0", "-c", "0", "-d", "5"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*GB")

    # check_linux_bandwith_usage -i lo -w 50 -c 90 -d 5 -f
    def test_warning_gb_perf_ok(self):
        args = ["-i", "lo", "-w", "1000000", "-c", "1000000", "-d", "5", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*GB")

    def test_warning_gb_perf_warning(self):
        args = ["-i", "lo", "-w", "0", "-c", "1000000", "-d", "5", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*GB")

    def test_warning_gb_perf_critical(self):
        args = ["-i", "lo", "-w", "0", "-c", "0", "-d", "5", "-f"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*GB")

     # check_linux_bandwith_usage -i lo -W 50 -C 90 -d 10 -l 500 -s /tmp/
    def test_warning_percent_path_ok(self):
        args = ["-i", "lo", "-W", "1000000", "-C", "1000000", "-d", "5", "-l", "1000000", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_path_warning(self):
        args = ["-i", "lo", "-W", "0", "-C", "1000000", "-d", "5", "-l", "1000000", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_path_critical(self):
        args = ["-i", "lo", "-W", "0", "-C", "0", "-d", "5", "-l", "1000000", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*% (.*/1000000.00GB)")

    # check_linux_bandwith_usage -i lo -W 50 -C 90 -d 10 -l 500 -f
    def test_warning_percent_perf_path_ok(self):
        args = ["-i", "lo", "-W", "1000000", "-C", "1000000", "-d", "5", "-l", "1000000", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_perf_path_warning(self):
        args = ["-i", "lo", "-W", "0", "-C", "1000000", "-d", "5", "-l", "1000000", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_percent_perf_path_critical(self):
        args = ["-i", "lo", "-W", "0", "-C", "0", "-d", "5", "-l", "1000000", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*% (.*/1000000.00GB)")

     # check_linux_bandwith_usage -i lo -w 50 -c 100 -d 10 -l 500 -f
    def test_warning_gb_limit_perf_path_ok(self):
        args = ["-i", "lo", "-w", "1000000", "-c", "1000000", "-d", "5", "-l", "1000000", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_gb_limit_perf_path_warning(self):
        args = ["-i", "lo", "-w", "0", "-c", "1000000", "-d", "5", "-l", "1000000", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*% (.*/1000000.00GB)")

    def test_warning_gb_limit_perf_path_critical(self):
        args = ["-i", "lo", "-w", "0", "-c", "0", "-d", "5", "-l", "1000000", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*% (.*/1000000.00GB)")

     # check_linux_bandwith_usage -i lo -w 50 -c 90 -d 5
    def test_warning_gb_path_ok(self):
        args = ["-i", "lo", "-w", "1000000", "-c", "1000000", "-d", "5", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*GB")

    def test_warning_gb_path_warning(self):
        args = ["-i", "lo", "-w", "0", "-c", "1000000", "-d", "5", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*GB")

    def test_warning_gb_path_critical(self):
        args = ["-i", "lo", "-w", "0", "-c", "0", "-d", "5", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*GB")

    # check_linux_bandwith_usage -i lo -w 50 -c 90 -d 5 -f
    def test_warning_gb_perf_path_ok(self):
        args = ["-i", "lo", "-w", "1000000", "-c", "1000000", "-d", "5", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 0, "OK: lo usage: .*GB")

    def test_warning_gb_perf_path_warning(self):
        args = ["-i", "lo", "-w", "0", "-c", "1000000", "-d", "5", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 1, "WARNING: lo usage: .*GB")

    def test_warning_gb_perf_path_critical(self):
        args = ["-i", "lo", "-w", "0", "-c", "0", "-d", "5", "-f", "-s", "/tmp/"]
        self.execute(Plugin, args, 0, "First use of plugin")
        self.execute(Plugin, args, 2, "CRITICAL: lo usage: .*GB")
