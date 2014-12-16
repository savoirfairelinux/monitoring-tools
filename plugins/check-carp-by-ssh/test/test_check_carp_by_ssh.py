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

import check_carp_by_ssh


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
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_carp_by_ssh""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_carp_by_ssh.py v%s"
                                     % check_carp_by_ssh.PLUGIN_VERSION)

    def test_bad_argument1(self):
        """Test bad argument:
            -1 192.168.1.10 -3 192.168.1.11 -c 172.16.1.2
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-1')
        sys.argv.append('192.168.1.10')
        sys.argv.append('-3')
        sys.argv.append('192.168.1.11')
        sys.argv.append('-c')
        sys.argv.append('172.16.1.2')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -3 not recognized")

    def test_bad_argument2(self):
        """Test bad argument:
            -1 192.168.1.10 -c 172.16.1.2
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-1')
        sys.argv.append('192.168.1.10')
        sys.argv.append('-c')
        sys.argv.append('172.16.1.2')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Argument `cross_ip_2' is missing !")

    def test_check1(self):
        """Test check1 :
            -1 192.168.1.10 -2 192.168.1.11 -c 172.16.1.2
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-1')
        sys.argv.append('192.168.1.10')
        sys.argv.append('-2')
        sys.argv.append('192.168.1.11')
        sys.argv.append('-c')
        sys.argv.append('172.16.1.2')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("CARP OK - Master cross ip: 192.168.1.10"
                                     " - Backup cross ip: 192.168.1.11"
                                     " - 3 interfaces up")

    def test_check2(self):
        """Test check2 :
            -1 192.168.1.12 -2 192.168.1.11 -c 172.16.1.2
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-1')
        sys.argv.append('192.168.1.12')
        sys.argv.append('-2')
        sys.argv.append('192.168.1.11')
        sys.argv.append('-c')
        sys.argv.append('172.16.1.2')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CARP ERROR - Bad number of carp interfaces")

    def test_check3(self):
        """Test check3 :
            -1 192.168.1.13 -2 192.168.1.11 -c 172.16.1.2
        """ 
        sys.argv = [sys.argv[0]]
        sys.argv.append('-1')
        sys.argv.append('192.168.1.13')
        sys.argv.append('-2')
        sys.argv.append('192.168.1.11')
        sys.argv.append('-c')
        sys.argv.append('172.16.1.2')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CARP ERROR - Plugin can get status of interfaces: ")

    def test_check4(self):
        """Test check4 :
            -1 192.168.1.14 -2 192.168.1.15 -c 172.16.1.2
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-1')
        sys.argv.append('192.168.1.14')
        sys.argv.append('-2')
        sys.argv.append('192.168.1.15')
        sys.argv.append('-c')
        sys.argv.append('172.16.1.2')
        try:
            out = StringIO()
            sys.stdout = out
            check_carp_by_ssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CARP ERROR - Interfaces in MASTER state are on the two hosts")



if __name__ == '__main__':
    unittest.main()
