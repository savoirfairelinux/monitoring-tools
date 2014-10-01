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

import os
import warnings
from random import shuffle
from subprocess import Popen, PIPE

import mock

from check_arp_no_change import Plugin, ArpRequest
from shinkenplugins import TestPlugin


class Test(TestPlugin):

    def test_version(self):
        self.execute(Plugin, ['-v'], 3, 'version ' + Plugin.VERSION)

    def test_help(self):
        self.execute(Plugin, ['-h'], 3, 'Usage:')

    def test_missing_host(self):
        self.execute(Plugin, [], 3, 'Host and MAC argument are required.')

    def test_missing_mac(self):
        self.execute(Plugin, ['-H', 'localhost'], 3, 'Host and MAC argument are required.')

    def test_ok_on_not_found(self):
        self.execute(Plugin, ['-H', '1.1.1.1', '-m', 'dont care', '--ok_on_not_found'],
                     0, 'ARP address not found but ok_on_not_found was set.')


class Test_ARP_with_arp_file(TestPlugin):

    def __init__(self, *a, **kw):
        super(Test_ARP_with_arp_file, self).__init__(*a, **kw)
        self._env = os.environ.copy()
        self._env['LANG'] = 'C'
        self._ip = None
        try:
            with open(ArpRequest.ARP_FILE) as fh:
                content = fh.readlines()
        except IOError as err:
            warnings.warn("Can't read ARP file (%s) some tests will be skipped." % ArpRequest.ARP_FILE)
        else:
            all_matches = []
            for line in content:
                line = line.rstrip('\n')
                match = ArpRequest._re_proc_net_arp.match(line)
                if match:
                    all_matches.append(match.groupdict())
            shuffle(all_matches)
            if not all_matches:
                warnings.warn("Could not parse any valid ARP entry from ARP file (%s) ; some tests will be skipped." % ArpRequest.ARP_FILE)
            else:
                gd = all_matches[0]
                self._ip, self._mac = gd['ip'], gd['mac']

    def test_ok(self):
        if self._ip:
            self.execute(Plugin, ('-H', self._ip, '-m', self._mac),
                     0, '^OK given MAC address corresponds to host')



#############################################################################
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

def _get_arp_file_content(self):
    for line in FAKE_ARP_DATA.split('\n'):
        yield line

#############################################################################

@mock.patch('check_arp_no_change.ArpRequest._get_arp_file_content', _get_arp_file_content)
class Test_ARP_mock(TestPlugin):

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

    def test_with_ping(self):
        self.execute(Plugin, ('-H', '172.17.0.12', '-i', 'eth1', '-m', 'e6:9e:ed:bc:b6:67', '-p'),
                     0, '^OK given MAC address corresponds to host')

#############################################################################

@mock.patch('sys.platform', 'win32')
@mock.patch('check_arp_no_change.ArpRequest._get_arp_file_content', _get_arp_file_content)
@mock.patch('check_arp_no_change.ArpRequest._can_read_arp_file', lambda self: False)
class Test_ARP_Windows(TestPlugin):
    def test_not_supported(self):
        self.execute(Plugin, ('-H', '172.17.0.12', '-i', 'eth1', '-m', 'e6:9e:ed:bc:b6:67'),
                     2, 'platform win32 not currently supported')

#############################################################################

@mock.patch('check_arp_no_change.ArpRequest._can_read_arp_file', lambda self: False)
class Test_ARP_with_arp_tool(TestPlugin):

    def __init__(self, *a, **kw):
        super(Test_ARP_with_arp_tool, self).__init__(*a, **kw)
        self._env = os.environ.copy()
        self._env['LANG'] = 'C'
        proc = Popen('arp -n', shell=True, stdout=PIPE)
        out, err = proc.communicate()
        for line in out.split('\n'):
            match = ArpRequest._re_usr_sbin_arp.match(line)
            if match:
                gd = match.groupdict()
                self._ip, self._mac = gd['ip'], gd['mac']
                break
        else:
            self._ip = None
            warnings.warn("Can't test with arp tool, arp call details: "
                          "out={out} err={err} RC={rc}".format(
                out=out, err=err, rc=proc.returncode
            ))

    def test_ok(self):
        if self._ip:
            self.execute(Plugin, ('-H', self._ip, '-m', self._mac),
                     0, '^OK given MAC address corresponds to host')

