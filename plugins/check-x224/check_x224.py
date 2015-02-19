#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
"""This plugin is made to test an x224 (RDP) service.
"""
#     Copyright (C) 2012 Savoir-Faire Linux Inc.
#
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program; if not, write to the Free Software
#     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# This Nagios plugin may be used to check the health of an RDP server, such
# as a Windows host offering remote desktop. Typically, a "strange" RDP
# response is a good indication of a Windows host is having trouble (while
# it is still responding to ping).

# It seems that the RDP protocol is based on a protocol called X.224,
# and this plugin only goes as far as checking very basic X.224
# protocol operations. Hence, the somewhat strange name of the plugin.

# Example of a check command definition, using this plugin:
# define command{
#         command_name    check_x224
#         command_line    /usr/local/nagios/check_x224 -H $HOSTADDRESS$
#         }
#
# A corresponding service definition might look like:
# define service{
#         service_description             Remote desktop
#         check_command                   check_x224
#         host_name                       somename.example.com
#         use                             generic-service
#         }

# Author: Troels Arvin <tra@sst.dk>
# Versioning:
# $Revision: 15676 $
# $Date: 2011-03-28 22:05:26 +0200 (Mon, 28 Mar 2011) $

# Copyright (c) 2011, Danish National Board of Health.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the  the Danish National Board of Health nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY the Danish National Board of Health ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL the Danish National Board of Health BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# References:
# TPKT:  http://www.itu.int/rec/T-REC-T.123/
# X.224: http://www.itu.int/rec/T-REC-X.224/en
#############################################################################

import socket
import struct
import time

#############################################################################

from shinkenplugins.old import BasePlugin

#############################################################################

default_rdp_port = 3389
default_warning_sec = 3
default_critical_sec = 50

#############################################################################
# x224 data..

l_expected_short = 11 # Older Windows hosts will return with a short answer
l_expected_long  = 19 # Newer Windows hosts will return with a longer answer

setup_x224_cookie = "Cookie: mstshash=\r\n"
setup_x224_rdp_neg_data = struct.pack(  # little-endian here, it seems ?
    '<BBHI',
    1, # type
    0, # flags
    8, # length
    3, # TLS + CredSSP
)
setup_x224_header = struct.pack(
    '!BBHHB',
    len(setup_x224_cookie)+6+8, # length,  1 byte
                                #  6: length of this header, excluding length byte
                                #  8: length of setup_x224_rdp_neg_data (static)
    224,                        # code,    1 byte (224 = 0xe0 = connection request)
    0,                          # dst-ref, 1 short
    0,                          # src-ref, 1 short
    0                           # class,   1 byte
)
setup_x224 = setup_x224_header + setup_x224_cookie + setup_x224_rdp_neg_data

tpkt_total_len = len(setup_x224) + 4
# 4 is the static size of a tpkt header
setup_tpkt_header = struct.pack(
    '!BBH',
    3,                          # version,  1 byte
    0,                          # reserved, 1 byte
    tpkt_total_len              # len,      1 short
)

setup_payload = setup_tpkt_header + setup_x224

teardown_payload = struct.pack(
    '!BBHBBBBBBB',
    3,                          # tpkt version,  1 byte
    0,                          # tpkt reserved, 1 byte
    11,                         # tpkt len,      1 short
    6,                          # x224 len,      1 byte
    128,                        # x224 code,     1 byte
    0,                          # x224 ?,        1 byte
    0,                          # x224 ?,        1 byte
    0,                          # x224 ?,        1 byte
    0,                          # x224 ?,        1 byte
    0                           # x224 ?,        1 byte
)


#############################################################################

class Plugin(BasePlugin):

    NAME = 'check_x224'
    VERSION = '0.1'
    DESCRIPTION = 'Checks an x224 (RDP) server.'
    AUTHOR = 'Grégory Starck'
    EMAIL = 'gregory.starck@savoirfairelinux.com'

    ARGS = [ # Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('V', 'version', 'display plugin version number', False),
            ('H', 'host', 'the host to check for its x224 service', True),
            ('p', 'port', 'the port to check, default=%s' % default_rdp_port, True),
            ('w', 'warning', 'number of seconds that an RDP response may take without'
                             ' emitting a warning status; default=%s' % default_warning_sec, True),
            ('c', 'critical', 'number of seconds that an RDP response may take without'
                              ' emitting a critical status; default=%s' % default_critical_sec, True),
    ]


    def check_args(self, args):

        if not args.get('help') and not args.get('version'):
            if not args.get('host'):
                return False, 'argument host is required'

        try:
            port = args['port'] = int(args.get('port', default_rdp_port))
            warning = args['warning'] = int(args.get('warning', default_warning_sec))
            critical = args['critical'] = int(args.get('critical', default_critical_sec))
        except ValueError:
            self.usage('port, warning and critical values must be integer values')

        if port < 0:
            self.usage(pre_msg='port number (%s) must be positive' % port)

        if (warning > critical):
            self.usage('warning seconds (%s) may not be greater than critical_seconds (%s)' % (warning, critical))

        return True, None

    def run(self, args):
        self.run2(**args)

    def run2(self, host, port, critical, warning, **kw):
        # make sure that we don't give up before critical sec has had a chance to elapse
        socket.setdefaulttimeout(critical+2)

        elapsed, data_received = self.x224_connect_and_read(host, port)

        l_data_received = len(data_received)
        if l_data_received not in (l_expected_short, l_expected_long):
            self.critical('x224 RDP response of unexpected length (%d)' % l_data_received)

        rec_tpkt_header = {}
        rec_x224_header = {}
        rec_nego_resp   = {}

        # Older Windows hosts will return with a short answer
        if len(data_received) == l_expected_short:
            rec_tpkt_header['version'],     \
            rec_tpkt_header['reserved'],    \
            rec_tpkt_header['length'],      \
                                            \
            rec_x224_header['length'],      \
            rec_x224_header['code'],        \
            rec_x224_header['dst_ref'],     \
            rec_x224_header['src_ref'],     \
            rec_x224_header['class'],       \
                = struct.unpack('!BBHBBHHB', data_received)
        else:
            # Newer Windows hosts will return with a longer answer
            rec_tpkt_header['version'],     \
            rec_tpkt_header['reserved'],    \
            rec_tpkt_header['length'],      \
                                            \
            rec_x224_header['length'],      \
            rec_x224_header['code'],        \
            rec_x224_header['dst_ref'],     \
            rec_x224_header['src_ref'],     \
            rec_x224_header['class'],       \
                                            \
            rec_nego_resp['type'],          \
            rec_nego_resp['flags'],         \
            rec_nego_resp['length'],        \
            rec_nego_resp['selected_proto'] \
                = struct.unpack('!BBHBBHHBBBHI', data_received)

        if rec_tpkt_header['version'] != 3:
            self.critical('Unexpected version-value(%d) in TPKT response' % rec_tpkt_header['version'])

        # 13 = binary 00001101; corresponding to 11010000 shifted four times
        # dst_ref=0 and class=0 was asked for in the connection setup
        if (rec_x224_header['code'] >> 4) != 13 or \
                rec_x224_header['dst_ref'] != 0 or \
                rec_x224_header['class'] != 0:
            self.critical('Unexpected element(s) in X.224 response')

        if elapsed > critical:
            self.critical('x224 RDP connection setup time (%f) was longer than (%d) seconds' % (elapsed, critical))

        if elapsed > warning:
            self.warning('x224 RDP connection setup time (%f) was longer than (%d) seconds' % (elapsed, warning))

        self.ok('x224 OK. Connection setup time: %f sec.|time=%fs;%d;%d;0' %
                (elapsed, elapsed, warning, critical))


    def _x224_connect_and_read(self, host, port):

        t1 = time.time()

        s = socket.socket()
        try:
            s.connect((host, port))
        except socket.gaierror as err:
            self.unknown("Could not connect on host '%s:%s' : %s" % (host, port, err))
        except Exception as err:
            self.critical("Could not connect on host '%s:%s' : %s" % (host, port, err))

        # TODO: we assume that the sent will be done in one shot,
        # which is not necessarily correct..
        sent_bytes = s.send(setup_payload)
        if sent_bytes != len(setup_payload):
            self.critical('Could not send x224 RDP setup payload')

        setup_received = s.recv(1024)

        t2 = time.time()

        # disconnect
        sent_bytes = s.send(teardown_payload)
        if sent_bytes != len(teardown_payload):
            self.critical('Could not send x224 RDP teardown payload')

        s.close()

        return t2 - t1, setup_received

    def x224_connect_and_read(self, host, port):
        try:
            return self._x224_connect_and_read(host, port)
        except Exception as err:
            self.critical('Unhandled error: %s' % err)



#############################################################################

def main():
    Plugin()

if __name__ == "__main__":
    main()

