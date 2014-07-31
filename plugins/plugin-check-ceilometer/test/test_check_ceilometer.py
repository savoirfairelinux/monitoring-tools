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
#            check_ceilometer A Nagios plug-in to use OpenStack Ceilometer API for metering
#
#
#  Author: Alexandre Viau <alexandre.viau@savoirfairelinux.com>
#
#

import unittest
import sys
#import os
import re
from StringIO import StringIO

sys.path.append("..")

import check_ceilometer


class TestPlugin(unittest.TestCase):
    def setUp(self):
        pass

    def test_help(self):
        """Test help output :
           -h
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-h')
        self.do_tst(3, """^check_ceilometer""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        self.do_tst(3, "^check_ceilometer.py v%s" % check_ceilometer.PLUGIN_VERSION)

    def test_argument_not_recognized(self):
        unknown_arg = '--test_unknown_arg'
        sys.argv = [sys.argv[0]]
        sys.argv.append(unknown_arg)
        self.do_tst(3, "option %s not recognized" % unknown_arg)

    def test_argument_missing(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append('--meter_name=some-meter-name')
        sys.argv.append('--warning=100')
        sys.argv.append('--critical=100')
        sys.argv.append('--os_username=admin')
        sys.argv.append('--os_password=admin')
        sys.argv.append('--os_tenant_name=demo')
        sys.argv.append('--os_auth_url=http://example.com/v2.0')
        self.do_tst(3, "Argument 'resource_id' is missing!")

    def test_argument_not_float(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append('--resource_id=some-ressource-id')
        sys.argv.append('--meter_name=some-meter-name')
        sys.argv.append('--warning=test')
        sys.argv.append('--critical=100')
        sys.argv.append('--os_username=test')
        sys.argv.append('--os_password=test')
        sys.argv.append('--os_tenant_name=test')
        sys.argv.append('--os_auth_url=http://example.com:9999')
        self.do_tst(3, "Argument 'warning': not float!")

    def test_authorization_failed(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append('--resource_id=some-ressource-id')
        sys.argv.append('--meter_name=some-meter-name')
        sys.argv.append('--warning=100')
        sys.argv.append('--critical=100')
        sys.argv.append('--os_username=test')
        sys.argv.append('--os_password=test')
        sys.argv.append('--os_tenant_name=test')
        sys.argv.append('--os_auth_url=http://127.0.0.1:9999')
        self.do_tst(3, "Authorization Failed")

    def do_tst(self, return_val, pattern_to_search):
        try:
            out = StringIO()
            sys.stdout = out
            check_ceilometer.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, return_val)
            output = out.getvalue().strip()
            matches = re.search(pattern_to_search, output)
            assert matches is not None

if __name__ == '__main__':
    unittest.main()
