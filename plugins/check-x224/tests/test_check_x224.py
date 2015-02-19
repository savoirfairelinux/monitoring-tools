#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#            test_check_x224
#
#
#  Author: Grégory Starck gregory.starck@savoirfairelinux.com
#
#

import sys
import unittest

#############################################################################

from shinkenplugins.tools.tests.netecho import NetEcho
from shinkenplugins.tools.tests.tests import TestPluginBase

from shinkenplugins.plugins.x224 import x224

#############################################################################

class TestPlugin(TestPluginBase):

    def setUp(self):
        self._main = x224.main

    def test_help(self):
        sys.argv = [sys.argv[0], '-h']
        self.do_tst(3, """^check_x224""")

    def test_version(self):
        sys.argv = [sys.argv[0], '-V']
        self.do_tst(3, "^check_x224 version %s" % x224.Plugin.VERSION)

    def test_default_args(self):
        sys.argv = [sys.argv[0]]
        self.do_tst(3, "host is required")

    def test_unknown_server(self):
        sys.argv = [sys.argv[0], '-H', 'kfljdqkljqsdkm']
        self.do_tst(3, "Name or service not known")

    def test_no_server(self):
        sys.argv = [sys.argv[0], '-H', 'localhost', '-p', '65535']
        self.do_tst(2, "Connection refused")

    def test_bad_opt(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append('--k')
        self.do_tst(3, "^option --k not recognized")


class TestPluginWithSocket(TestPluginBase):

    def setUp(self):
        self._main = x224.main
        self.nc = NetEcho(host='localhost')
        self.nc.start()

    def tearDown(self):
        self.nc.join()

    def test_bad_rsp_length(self):
        self.nc.echo = "BAD X224 LENGTH" # not 11 nor 19 ..
        sys.argv = [sys.argv[0], '-H', 'localhost', '-p', str(self.nc.port)]
        self.do_tst(2, "^x224 RDP response of unexpected length \(15\)$")

    def test_bad_version(self):
        self.nc.echo = "A" * 11
        sys.argv = [sys.argv[0], '-H', 'localhost', '-p', str(self.nc.port)]
        self.do_tst(2, "Unexpected version-value")

    def test_bad_elements(self):
        self.nc.echo = "\x03" + "A"*10
        sys.argv = [sys.argv[0], '-H', 'localhost', '-p', str(self.nc.port)]
        self.do_tst(2, "Unexpected element\(s\)")

    def test_good_connection(self):
        self.nc.echo = '\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x01\x08\x00\x02\x00\x00\x00'
        sys.argv = [sys.argv[0], '-H', 'localhost', '-p', str(self.nc.port)]
        self.do_tst(0, "^x224 OK.")


if __name__ == '__main__':
    unittest.main()
