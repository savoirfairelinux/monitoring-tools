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

import check_libvirt_stats


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
            check_libvirt_stats.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_libvirt_stats""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_libvirt_stats.py v%s"
                                     % check_libvirt_stats.PLUGIN_VERSION)


    def test_bad_arguments1(self):
        """Test bad arguments 1 :
           -f
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-f')
        sys.argv.append('127.0.0.1')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -f not recognized")

    def test_fake_check(self):
        """Test fake check2 :
           -U GB -u test:///default -w 760% -c 790% 
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-U')
        sys.argv.append('MB')
        sys.argv.append('-u')
        sys.argv.append('test:///default')
        sys.argv.append('-w')
        sys.argv.append('760')
        sys.argv.append('-c')
        sys.argv.append('800')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            assert output.startswith('OK')

    def test_fake_check(self):
        """Test fake check1 :
           -U TB -u test:///default -w 760 -c 790
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-U')
        sys.argv.append('MB')
        sys.argv.append('-u')
        sys.argv.append('test:///default')
        sys.argv.append('-w')
        sys.argv.append('760')
        sys.argv.append('-c')
        sys.argv.append('800')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            assert output.startswith('OK')


    def test_bad_arguments2(self):
        """Test bad arguments2 :
           -U GB -u test:///default -w 80% -c 79% 
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-U')
        sys.argv.append('MB')
        sys.argv.append('-u')
        sys.argv.append('test:///default')
        sys.argv.append('-w')
        sys.argv.append('80')
        sys.argv.append('-c')
        sys.argv.append('79')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            assert output.startswith('Warning threshold must be less than')


    def test_bad_arguments3(self):
        """Test bad arguments3 :
           -U GB -u test:///default
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-U')
        sys.argv.append('MB')
        sys.argv.append('-u')
        sys.argv.append('test:///default')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            assert output.startswith("Argument `warning' is missing !")

    def test_bad_arguments4(self):
        """Test bad arguments4 :
           -U GB -u test:///default
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-U')
        sys.argv.append('sdgsd')
        sys.argv.append('-u')
        sys.argv.append('test:///default')
        sys.argv.append('-w')
        sys.argv.append('80')
        sys.argv.append('-c')
        sys.argv.append('81')
        try:
            out = StringIO()
            sys.stdout = out
            check_libvirt_stats.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            assert output.startswith("Unit : bad format !")



if __name__ == '__main__':
    unittest.main()
