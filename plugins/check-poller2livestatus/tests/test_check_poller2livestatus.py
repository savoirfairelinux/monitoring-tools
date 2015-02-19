#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright (C) 2012 Savoir-Faire Linux Inc.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Projects :
#            Shinken plugins
#
#  File :
#            check_poller2livestatus Check Shinken from poller to livestatus module
#
#
#  Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import unittest
import sys
import time


from shinkenplugins.plugins.poller2livestatus import poller2livestatus


from shinkenplugins.tools.tests.netecho import NetEcho
from shinkenplugins.tools.tests.tests import TestPluginBase

class TestPlugin(TestPluginBase):
    def setUp(self):
        self._main = poller2livestatus.main

    def test_help(self):
        """Test help output :
           -h
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-h')
        self.do_tst(3, """^check_poller2livestatus""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        self.do_tst(3, "^check_poller2livestatus.py v%s" % poller2livestatus.PLUGIN_VERSION)

    def test_connection(self):
        """Test connection :
        -B 127.0.0.1 -H myhost -p mypoller
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        self.do_tst(2, "Error while connecting to livestatus")

    def test_bad_arguments_1(self):
        """Test Bad arguments 1 :
        -B 127.0.0.1 -P 50001 -S myservice -p mypoller
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-P')
        sys.argv.append('50001')
        sys.argv.append('-S')
        sys.argv.append('myservice')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        self.do_tst(3, "Argument 'hostname'")

    def test_bad_arguments_2(self):
        """Test Bad arguments 2 :
        -B 127.0.0.1 -H myhost -p mypoller -P mybadport
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        sys.argv.append('-P')
        sys.argv.append('mybadport')
        self.do_tst(3, "Argument `broker-port'")

    def test_bad_arguments_3(self):
        """Test Bad arguments 3 :
        -B 127.0.0.1 -H myhost -p mypoller -w 60 -c 55
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        sys.argv.append('-w')
        sys.argv.append('60')
        sys.argv.append('-c')
        sys.argv.append('55')
        self.do_tst(3, "Warning threshold must be less than CRITICAL threshold")

    def test_bad_arguments_4(self):
        """Test Bad arguments 4 :
        -B 127.0.0.1 -H myhost -w 60 -c bad_critical
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-w')
        sys.argv.append('60')
        sys.argv.append('-c')
        sys.argv.append('bad_critical')
        self.do_tst(3, "Argument `critical': Bad format !")


class TestPluginWithSocket(TestPluginBase):
    def setUp(self):
        self._main = poller2livestatus.main
        self.nc = NetEcho(host='localhost', port=50001)
        self.nc.start()

    def tearDown(self):
        self.nc.join()

    def test_connection_ok(self):
        """Test connection ok :
        -B localhost -P 50001 -H myhost -S myservice -p mypoller
        """
        now = int(time.time())
        self.nc.echo = 'myhost;myservice;%d;5' % now

        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('localhost')
        sys.argv.append('-P')
        sys.argv.append('50001')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-S')
        sys.argv.append('myservice')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        self.do_tst(0, "")


    def test_connection_ok_check(self):
        """Test connection ok check :
        -B 127.0.0.1 -P 50001 -H myhost -S myservice -p mypoller -C mybroker
        """
        now = int(time.time())
        self.nc.echo = 'myhost;myservice;%d;5' % now

        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-P')
        sys.argv.append('50001')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-S')
        sys.argv.append('myservice')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        sys.argv.append('-C')
        sys.argv.append('mybroker')
        self.do_tst(0, "| delta=")

    def test_connection_warning(self):
        """Test connection warning
        -B 127.0.0.1 -H myhost -S myservice -p mypoller -w 60 -c 120
        """
        now = int(time.time()) - 65
        self.nc.echo = 'myhost;myservice;%d;5' % now

        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('localhost')
        sys.argv.append('-P')
        sys.argv.append('50001')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-S')
        sys.argv.append('myservice')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        sys.argv.append('-w')
        sys.argv.append('60')
        sys.argv.append('-c')
        sys.argv.append('120')
        self.do_tst(1, "# delta:6[0-9]")

    def test_connection_critical(self):
        """Test connection critical
        -B 127.0.0.1 -H myhost -p mypoller -w 60 -c 120
        """
        now = int(time.time()) - 155
        self.nc.echo = 'myhost;%d;5' % now

        sys.argv = [sys.argv[0]]
        sys.argv.append('-B')
        sys.argv.append('localhost')
        sys.argv.append('-P')
        sys.argv.append('50001')
        sys.argv.append('-H')
        sys.argv.append('myhost')
        sys.argv.append('-p')
        sys.argv.append('mypoller')
        sys.argv.append('-w')
        sys.argv.append('60')
        sys.argv.append('-c')
        sys.argv.append('120')
        self.do_tst(2, "# delta:15[0-9]")



if __name__ == '__main__':
    unittest.main()
