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

# Copyright (C) 2014, Grégory Starck <gregory.starck@savoirfairelinux.com>

#############################################################################

from shinkenplugins import BasePlugin, STATES

DEFAULT_IFNAME = "eth0"

#############################################################################

import os
import sys
import subprocess

class ArpRequest:

    def __init__(self, ipaddr, if_name, _arp_cmd="arp -i {if_name} -a {ipaddr}"):
        self.ipaddr = ipaddr
        self.if_name = if_name
        self._arp_cmd = _arp_cmd

    def request(self):
        ipaddr = self.ipaddr
        cmd = self._arp_cmd.format(if_name=self.if_name, ipaddr=self.ipaddr)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output, errors = p.communicate()
        # should we check return_code
        # though not sure every implementation of `arp´ has the same behaviour..
        if output is not None:
            if sys.platform in ['linux', 'linux2']:
                for i in output.split("\n"):
                    if ipaddr in i:
                        for j in i.split():
                            if ":" in j:
                                return j

            elif sys.platform in ['win32']:
                item = output.split("\n")[-2]
                if ipaddr in item:
                    return item.split()[1]


#############################################################################

class Plugin(BasePlugin):
    NAME = 'check-arp-no-change'
    VERSION = '0.1'
    DESCRIPTION = "Verify that a host MAC address hasn't changed"
    AUTHOR = 'Grégory Starck'
    EMAIL = 'gregory.starck@savoirfairelinux.com'
    
    ARGS = [
        ('h', 'help', 'display plugin help', False),
        ('v', 'version', 'display plugin version number', False),
        # Hammer time^W^W Add your plugin arguments here:
        # ('short', 'long', 'description', 'does it expect a value?')
        ('H', 'host', 'The host to check', True),
        ('m', 'mac', 'The MAC address the host should have', True),
        #('c', 'critical', "If ARP doesn't match then return a warning ; default is to return a warning.", False),
        #('w', 'warn-on-not-found', "If ARP isn't found (timeout) then force a warning return.", False),
        ('i', 'if_name', 'Explicitly specify the interface name on which to look for the ARP address. default='+DEFAULT_IFNAME, False),
        ('p', 'ping_before', 'Do you want me to ping the host before reading its ARP address ?', False)
    ]
    
    def check_args(self, args):
        host = args.get('host')
        mac = args.get('mac')
        args['if_name'] = args.get('if_name', DEFAULT_IFNAME)
        if not (host and mac):
            self.unknown('Host and MAC argument are required.')
        args['mac'] = mac.lower()
        args['ping_before'] = 'ping_before' in args
        return True, None

    def run2(self, host, mac, if_name, ping_before=False, **kw):
        if ping_before:
            os.popen('ping -W 2 -c 1 %s' % host)
        r = ArpRequest(host, if_name=if_name)
        mac_read = r.request()
        if mac_read:
            if mac != mac_read:
                self.critical("MAC address for host %s = %s doesn't match "
                              "the expected one (%s)" % (host, mac_read, mac))
        else:
            self.warning('ARP address not found for host %s' % host)

    def run(self, args):
        self.run2(**args)
        self.ok('OK given MAC address corresponds to host')

#############################################################################

if __name__ == "__main__":
    Plugin()
