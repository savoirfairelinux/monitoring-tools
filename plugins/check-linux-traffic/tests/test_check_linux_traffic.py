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
import tempfile

import netifaces

from shinkenplugins.plugins.linux_traffic import linux_traffic


orig_linux_traffic_main = linux_traffic.main


class TestPlugin(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='tests_linux_traffic')
        shutil.rmtree(self.tmpdir, True)
        self.interfaces = netifaces.interfaces()
        self.interfaces = filter(lambda x: ':' not in x, self.interfaces)
        if len(self.interfaces) == 0:
            print('Error: No interface found.')
            sys.exit(1)

        def mocked_main(argv):
            argv.extend(('--store_dir', self.tmpdir))
            return orig_linux_traffic_main(argv)

        linux_traffic.main = mocked_main


    def test_help(self):
        """Test help output :
           -h
        """
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-h'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_linux_traffic""")

    def test_version(self):
        """Test version output :
           -V
        """
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-v'])
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
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-n', self.interfaces[0]])
        except SystemExit, e:
            self.assertEquals(e.code, 0, str(e))
            output = out.getvalue().strip()
            assert output == "Waiting next check to get data..."

        time.sleep(5)
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-f', '-n', self.interfaces[0]])
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
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['--ignore-lo', '-f'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output == "Waiting next check to get data..."
        time.sleep(5)
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['--ignore-lo', '-f'])
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
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-f', '-n', self.interfaces[0], '-l', '131072000'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output == "Waiting next check to get data..."
        time.sleep(5)
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-f', '-n', self.interfaces[0], '-l', '131072000'])
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
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-g'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -g not recognized")

    def test_bad_arguments2(self):
        """Test bad arguments2:
           -w 80 -c 70
        """
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-w', '80', '-c', '70'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Critical threshold must be greater than warning threshold")

    def test_bad_arguments3(self):
        """Test bad arguments3:
           -w 80
        """
        try:
            out = StringIO()
            sys.stdout = out
            linux_traffic.main(['-w', 80])
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
            linux_traffic.main(['-w', 'bad_arg'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad argument: ")




if __name__ == '__main__':
    unittest.main()
