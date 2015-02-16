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

#############################################################################

import os
import sys
import re
import subprocess
import warnings

_is_supported_platform = sys.platform in ('linux', 'linux2')
if not _is_supported_platform:
    warnings.warn('%s is not a supported platform' % sys.platform)

#############################################################################
_environ = os.environ.copy()
_environ['LANG'] = 'C'

class ArpRequest(object):

    ARP_FILE = '/proc/net/arp' # obviously for linux only

    _mac_regex = ':'.join(['[0-9a-fA-F]{2}']*6)   # a valid MAC address is 6 hexa chars separated by ':'
    _mac_re = re.compile(_mac_regex)

    _ip_regex = '\.'.join(['\d+']*4)             # a valid IP address is 4 integers separated by '.'
    _ip_re = re.compile(_ip_regex)

    _null_mac = ':'.join(6 * ('00',))            # the null MAC

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

    def __init__(self, ipaddr, if_name, _arp_cmd=None):
        self.ipaddr = ipaddr
        self.if_name = if_name
        if _arp_cmd is None:
            _arp_cmd = ['arp', '-n']
        if if_name:
            _arp_cmd.extend(('-i', self.if_name))
        self._arp_cmd = _arp_cmd

    def __repr__(self):
        return '<%s ipaddr=%s if_name=%s />' % (self.__class__.__name__, self.ipaddr, self.if_name)

    def _can_read_arp_file(self):
        try:
            with open(self.ARP_FILE):
                return True
        except IOError:
            return False

    def _get_arp_file_content(self):
        '''
        :return: a generator which yields the lines of the ARP_FILE. Minus its first header line.
        Each yielded line is right stripped.
        '''
        with open(self.ARP_FILE) as fh:
            fh.readline()       # skip header
            for line in fh:
                yield line.rstrip('\n')

    def _get_arp_bin_content(self):
        '''
        :return: a list of the lines (right stripped) found in the output of `arp´ tool.
        So the first line of the output is removed from the result.
        '''
        p = subprocess.Popen(self._arp_cmd, shell=False, stdout=subprocess.PIPE, env=_environ)
        output, errors = p.communicate()
        if errors:
            pass # TODO: do what ?
        lines = output.split('\n')
        return lines[1:]

    def request(self):
        '''Execute the ARP request.
If "/proc/net/arp" (self.ARP_FILE) is readable then directly read the arp table from there.
Otherwise execute an 'arp' call.

:return: a generator which yields dictionary corresponding to MAC addresses found and
that match the requested IP address, and interface name if provided. The yielded dictionaries
have the following keys:
    'mac':      will contain the MAC in str form ("aa:bb:cc:dd:ee:ff")
    'ip' :      the request ipaddress
    'device':   the device on which the mac was found.'''
        if self._can_read_arp_file():
            regex, content = self._re_proc_net_arp, self._get_arp_file_content()
        else:
            content = self._get_arp_bin_content()
            if _is_supported_platform:
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
            # don't forget to ignore "null" ARP addresses:
            if gd['mac'] == self._null_mac:
                continue
            # and ignore non matching device/interface name if an explicit one was provided.
            if self.if_name and gd['device'] != self.if_name:
                continue
            yield gd


#############################################################################

class Plugin(BasePlugin):
    NAME = 'check-arp-no-change'
    VERSION = '0.2'
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
        ('i', 'if_name', 'Explicitly specify the interface name on which to look for the ARP address. '
        # TODO: Feature enhancement:
        #                 'This option can be given many times to give multiple interfaces name to look on.'
                         'Default is to look on all interfaces '
                         'and if at least one of them matches the given MAC then returns an OK.', True),
        # TODO: Feature enhancement:
        #('', 'ignore_if_name', 'Ignore MAC adresses from this interface name.'
        #                       'Use multiple times to ignore many interfaces.', True),
        ('n', 'no_ping_before', 'Do you want me to NOT ping the host before reading its ARP address ?'
                             'Default is to ping before reading the ARP table.', False),
        ('s', 'status_on_no_ip', 'What status to return when no ip address matches the requested one.\n'
                                    '   ok: return an OK\n',
                                    '   warn: return a WARNING (default)\n.'
                                    '   crit: return a CRITICAL one' , True)
        # TODO: Feature enhancement:
        #('', 'action_on_many_arp_adress', 'Give the action to do in case the requested ip is present on multiple interfaces.\n'
        #                                  '"default" (without the quotes): like "ok".\n'
        #                                  '"ok" : Returns an OK if at least one matches.\n'
        #                                  '"warn" : Returns a WARNING if at least one matches.\n', True)

    ]


    _status2method = {
        'ok':       BasePlugin.ok,
        'warn':     BasePlugin.warning,
        'warning':  BasePlugin.warning,
        'crit':     BasePlugin.critical,
        'critical': BasePlugin.critical,
        'unk':      BasePlugin.unknown,
        'unknown':  BasePlugin.unknown,
    }

    def check_args(self, args):
        host = args.get('host')
        mac = args.get('mac')
        if not (host and mac):
            self.unknown('Host address and MAC argument are required.')
        args['mac'] = mac.lower()
        if not ArpRequest._ip_re.match(host):
            self.unknown("Host address (%s) doesn't looks like a valid IPv4. I absolutely need an IP address !" % host)
        status_on_no_ip = self._status2method.get(args.get('status_on_no_ip',
                                                           'warning'), None)
        if status_on_no_ip is None:
            self.unknown('Invalid value for status_on_no_ip: %r' % status_on_no_ip)
        args['status_on_no_ip'] = status_on_no_ip
        args['ping_before'] = 'no_ping_before' not in args

        if not _is_supported_platform:
            self.unknown('Platform %s not currently supported, '
                         'please submit a feature request' % sys.platform)
        return True, None

    @staticmethod
    def ping(host, timeout=1, count=2):
        cmd = 'ping -n -W {timeout} -c {count} {host}'.format(
            host=host, timeout=timeout, count=count)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        proc.communicate()

    def run2(self, host, mac, if_name=None, ping_before=True,
             status_on_no_ip=BasePlugin.warning, **kw):
        if ping_before:
            self.ping(host)
        r = ArpRequest(host, if_name=if_name)
        results = tuple(r.request())
        if not results:
            msg = 'No ARP address found for host=%s. (and status_on_no_ip=%s)' % (
                host, status_on_no_ip.__name__)
            return status_on_no_ip(self, msg)

        goods = []
        for data in results:
            mac_read = data.get('mac', '')
            if mac == mac_read.lower(): # double make sure we compare lower case
                goods.append(data)      # (mac has been lowered case in check_args)
        if not goods:
            mac_reads = ','.join(data.get('mac') for data in results)
            self.critical("Some ARP address(es) was(were) found for host %s ( %s ) but none match "
                          "the expected one (%s)" % (host, mac_reads, mac))
        if len(goods) > 1:
            # TODO?: wow, quite unusual ..
            pass

    def run(self, args):
        #print(args)
        self.run2(**args)
        self.ok('OK given MAC address corresponds to host')

#############################################################################

def main(argv=None):
    Plugin(argv)


if __name__ == "__main__":
    main()
