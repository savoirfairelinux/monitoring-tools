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

# Copyright (C) 2014, Grégory Starck <gregory.starck@savoirfairelinux.com>
import unittest
from unittest.case import skip

import check_arp_no_change
from check_arp_no_change import Plugin

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


# removed header line from this fake arp data:
# (Address                  HWtype  HWaddress           Flags Mask            Iface)
FAKE_ARP_DATA = '''\
172.17.0.12      0x1         0x0         e6:9e:ed:bc:b6:67     *        eth1
192.168.50.1     0x1         0x2         00:21:a1:39:96:40     *        eth0
172.17.0.15      0x1         0x2         2e:d6:1b:d0:f6:e0     *        wlan0
172.17.0.8       0x1         0x2         72:7d:5f:ca:03:5a     *        wlan1
172.17.0.11      0x1         0x2         36:57:18:09:4e:09     *        eth0
172.17.0.14      0x1         0x2         1e:0e:8e:6b:5d:32     *        eth0
172.17.0.4       0x1         0x2         96:5d:d9:ee:54:05     *        eth0'''


class Test_ARP_mock(TestPlugin):

    def make_ArpRequest(self, content):
        class ArpRequest(check_arp_no_change.ArpRequest):
            def _get_arp_file_content(self):
                for line in content:
                    yield line
        return ArpRequest

    def setUp(self):
        check_arp_no_change.ArpRequest = self.make_ArpRequest(FAKE_ARP_DATA.split('\n'))

    def tearDown(self):
        pass


    def test_unknown_interface(self):
        self.execute(Plugin, ('-H', '172.17.0.12', '-i', 'no_such_if', '-m', '00:21:a1:39:96:40'),
                     1, 'ARP address not found')

    def test_no_arp(self):
        self.execute(Plugin, ('-H', '172.17.0.8', '-i', 'eth0', '-m', '00:21:a1:39:96:40'),
                     1, 'ARP address not found')

    def test_mac_changed(self):
        self.execute(Plugin, ('-H', '172.17.0.12', '-i', 'eth1', '-m', '00:21:a1:39:96:41'),
                     2, "MAC address for host .* doesn't match the expected one")

    def test_ok(self):
        self.execute(Plugin, ('-H', '172.17.0.12', '-i', 'eth1', '-m', 'e6:9e:ed:bc:b6:67'),
                     0, '^OK given MAC address corresponds to host')

