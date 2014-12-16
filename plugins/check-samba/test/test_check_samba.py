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
#  Projects :
#            Shinken plugins
#
#  File :
#            create_new_plugin.sh Create new shinken plugin from template
#
#
#  Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import unittest
import sys
import os
from StringIO import StringIO

sys.path.append("..")

import check_samba


class TestPlugin(unittest.TestCase):
    def setUp(self):
        pass

    def test_help(self):
        """Test help output :
           -h
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-h')
        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_samba""")

    def test_bad_options(self):
        """Test check_args :
           -X
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-X')
        
        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""option """)

    def test_bad_ip(self):
        """Test bad_ip :
           -H 992.168.50.254 -s test_shinken
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.50.254')
        sys.argv.append('-s')
        sys.argv.append('test_shinken')
        
        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("""CRITICAL - UNKNOWN Ip address :""")

    def test_bad_hostname(self):
        """Test bad_hostname :
           -H foo-bar -s test_shinken
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('foo-bar')
        sys.argv.append('-s')
        sys.argv.append('test_shinken')
        
        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("""CRITICAL - Can't connect to """)

    def test_bad_values(self):
        """Test bad_values :
           -H 192.168.50.23 -s test_shinken
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.50.23')
        sys.argv.append('-s')
        sys.argv.append('test_shinken')
        sys.argv.append('-w')
        sys.argv.append('10')
        sys.argv.append('-c')
        sys.argv.append('9')

        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""UNKNOWN - Wrong warning, critical or timeout values""")

    def test_check_args_mendatory(self):
        """Test check_args_mendatory :
           -<empty>
        """
        sys.argv = [sys.argv[0]]

        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""UNKNOWN - Argument '""")

    def test_check_args_couple(self):
        """Test check_args_couple :
           -H 
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.50.23')
        sys.argv.append('-s')
        sys.argv.append('test_shinken')
        sys.argv.append('-w')
        sys.argv.append('10')

        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""UNKNOWN - You can't specify only warning or critical.""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_samba.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_samba.py v%s"
                                     % check_samba.PLUGIN_VERSION)


if __name__ == '__main__':
    unittest.main()
