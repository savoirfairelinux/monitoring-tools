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
import time
import os
import shutil
from StringIO import StringIO

import netifaces

from shinkenplugins.plugins import linux_traffic


class TestPlugin(unittest.TestCase):
    def setUp(self):
        shutil.rmtree("/tmp/check_linux_traffic", True)
        reload(linux_traffic)

        self.interfaces = netifaces.interfaces()
        self.interfaces = filter(lambda x: ':' not in x, self.interfaces)
        if len(self.interfaces) == 0:
            print('Error: No interface found.')
            sys.exit(1)

    def test_help(self):
        """Test help output :
           -h
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-h')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_linux_traffic""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_linux_traffic.py v%s"
                                     % linux_traffic.PLUGIN_VERSION)

    def test_check2(self):
        """Test check2:
           -n `first interface`
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-n')
        sys.argv.append(self.interfaces[0])
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(e.code, 0, str(e))
            output = out.getvalue().strip()
            assert output == "Waiting next check to get data..."
        time.sleep(5)
        sys.argv = [sys.argv[0]]
        sys.argv.append('-f')
        sys.argv.append('-n')
        sys.argv.append(self.interfaces[0])
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.find(self.interfaces[0]) != -1
            if len(self.interfaces) >= 2:
                assert output.find(self.interfaces[1]) == -1

    def test_check3(self):
        """Test check3:
           -f --ignore-lo
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--ignore-lo')
        sys.argv.append('-f')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output == "Waiting next check to get data..."
        sys.argv = [sys.argv[0]]
        sys.argv.append('--ignore-lo')
        sys.argv.append('-f')
        time.sleep(5)
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.find("lo") == -1
            assert output.find("|") != -1

    def test_check4(self):
        """Test check4:
           -f -n `first interface` -l 131072000 
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-f')
        sys.argv.append('-n')
        sys.argv.append(self.interfaces[0])
        sys.argv.append('-l')
        sys.argv.append('131072000')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output == "Waiting next check to get data..."
        time.sleep(5)
        sys.argv = [sys.argv[0]]
        sys.argv.append('-f')
        sys.argv.append('-n')
        sys.argv.append(self.interfaces[0])
        sys.argv.append('-l')
        sys.argv.append('131072000')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.find(self.interfaces[0]) != -1
            assert output.find("131072000") != -1

    def test_bad_arguments1(self):
        """Test bad arguments1:
           -g
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-g')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -g not recognized")

    def test_bad_arguments2(self):
        """Test bad arguments2:
           -w 80 -c 70
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-w')
        sys.argv.append('80')
        sys.argv.append('-c')
        sys.argv.append('70')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Critical threshold must be greater than warning threshold")

    def test_bad_arguments3(self):
        """Test bad arguments3:
           -w 80
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-w')
        sys.argv.append('80')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Critical threshold and warning threshold must be define")

    def test_bad_arguments4(self):
        """Test bad arguments4:
           -w bad_arg
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-w')
        sys.argv.append('bad_arg')
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad argument: ")




if __name__ == '__main__':
    unittest.main()
