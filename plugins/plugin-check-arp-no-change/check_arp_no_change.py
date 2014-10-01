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
import re
import subprocess
import warnings

if sys.platform not in ['linux', 'linux2']:
    warnings.warn('%s is not a supported platform' % sys.platform)

#############################################################################
_environ = os.environ.copy()
_environ['LANG'] = 'C'

class ArpRequest:

    ARP_FILE = '/proc/net/arp' # obviously for linux only

    _mac_regex = ':'.join(['\w{2}']*6)
    _ip_regex = '\.'.join(['\d+']*4)

    _re_proc_net_arp = re.compile(
        '^'
        '(?P<ip>'+_ip_regex+')'     # ip
        '\s+'
        '[^\s]+'                    # HW type
        '\s+'
        '[^\s]+'                    # flags
        '\s+'
        '(?P<mac>'+_mac_regex+')'   # MAC/HW address
        '\s+'
        '[^\s]+'                    # Mask
        '\s+'
        '(?P<device>[^\s]+)'        # Device
        '$'
    )

    _re_usr_sbin_arp = re.compile(
        '^'
        '(?P<ip>'+_ip_regex+')'    # Address
        '\s+'
        '[^\s]+'                    # HWtype
        '\s+'
        '(?P<mac>'+_mac_regex+')'   # HWaddress
        '\s+'
        '[^\s]+'                    # Flags
        '\s+'
        '(?P<device>[^\s]+)'        # Device
        '$'
    )

    def __init__(self, ipaddr, if_name, _arp_cmd=["arp", "-i", "{if_name}", "{ipaddr}"]):
        self.ipaddr = ipaddr
        self.if_name = if_name
        self._arp_cmd = _arp_cmd

    def __repr__(self):
        return '<%s ipaddr=%s if_name=%s />' % (self.__class__.__name__, self.ipaddr, self.if_name)

    def _can_read_arp_file(self):
        try:
            with open(self.ARP_FILE):
                return True
        except Exception:
            return False

    def _get_arp_file_content(self):
        with open(self.ARP_FILE) as fh:
            fh.readline() # skip header
            for line in fh:
                yield line.rstrip('\n')

    def _get_arp_bin_content(self):
        df = { 'if_name': self.if_name, 'ipaddr': self.ipaddr }
        cmd_args = tuple(a.format(**df) for a in self._arp_cmd)
        p = subprocess.Popen(cmd_args, shell=False, stdout=subprocess.PIPE, env=_environ)
        output, errors = p.communicate()
        if errors:
            pass # do what ?
        return output.split('\n')


    def request(self):
        '''Execute the ARP request.
If /proc/net/arp is readable then directly read the arp table from there.
Otherwise execute an 'arp' call.

:return: a dictionnary with following keys:
    'mac': will contain the MAC in str form ("aa:bb:cc:dd:ee:ff")
    'ip' : the request ipaddress
    'device: the device on which the mac was found.'''
        if self._can_read_arp_file():
            regex, content = self._re_proc_net_arp, self._get_arp_file_content()
        else:
            content = self._get_arp_bin_content()
            if sys.platform in ['linux', 'linux2']:
                regex = self._re_usr_sbin_arp
            else:
                raise RuntimeError('platform %s not currently supported.' % sys.platform)
            # TODO: elif sys.platform in ['win32']:
            #   pass

        for line in content:
            match = regex.match(line)
            if not match:
                continue
            gd = match.groupdict()
            if gd['ip'] != self.ipaddr:
                continue
            if ((self.if_name and gd['device'] == self.if_name)
                or not self.if_name
            ):
                return gd




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
        ('i', 'if_name', 'Explicitly specify the interface name on which to look for the ARP address. default='+DEFAULT_IFNAME, True),
        ('p', 'ping_before', 'Do you want me to ping the host before reading its ARP address ?', False),
        ('_', 'ok_on_not_found', 'Return an OK status code on no MAC found. Default is to return a WARNING status code.', False),

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

    @staticmethod
    def ping(host, timeout=1, count=2):
        cmd = 'ping -W {timeout} -c {count} {host}'.format(**locals())
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        proc.communicate()

    def run2(self, host, mac, if_name, ping_before=False, **kw):
        if ping_before:
            self.ping(host)
        r = ArpRequest(host, if_name=if_name)
        data = r.request()
        if data:
            mac_read = data.get('mac', '')
            if mac != mac_read:
                self.critical("MAC address for host %s = %s doesn't match "
                              "the expected one (%s)" % (host, mac_read, mac))
        else:
            if 'ok_on_not_found' in kw:
                self.ok('ARP address not found but ok_on_not_found was set.')
            else:
                self.warning('ARP address not found for host %s' % host)

    def run(self, args):
        self.run2(**args)
        self.ok('OK given MAC address corresponds to host')

#############################################################################

if __name__ == "__main__":
    Plugin()
