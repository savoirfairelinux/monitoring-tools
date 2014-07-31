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

import check_wanpipe


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
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_wanpipe""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_wanpipe.py v%s"
                                     % check_wanpipe.PLUGIN_VERSION)

    def test_bad_arguments1(self):
        """Test bad arguments1:
        """
        sys.argv = [sys.argv[0]]
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Argument `channels' is missing !")


    def test_bad_arguments2(self):
        """Test bad arguments2:
           -i w1g1 -f -s 8 -w 4 -c 5
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-i')
        sys.argv.append('w1g1')
        sys.argv.append('-f')
        sys.argv.append('-s')
        sys.argv.append('8')
        sys.argv.append('-w')
        sys.argv.append('4')
        sys.argv.append('-c')
        sys.argv.append('5')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Warning argument but be greater "
                                     "than critical argument")

    def test_bad_arguments3(self):
        """Test bad arguments3:
           -s bad
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-s')
        sys.argv.append('bad')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad format for argument: ")

    def test_check1(self):
        """Test check1:
           -i w1g1 -f -s 5 -w 4 -c 5
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-i')
        sys.argv.append('w1g1')
        sys.argv.append('-f')
        sys.argv.append('-s')
        sys.argv.append('5')
        sys.argv.append('-w')
        sys.argv.append('2')
        sys.argv.append('-c')
        sys.argv.append('1')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK - 3/5 channels in OK state")


    def test_check2(self):
        """Test check2:
           -i w1g1 -s 4 -w 2 -c 1
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-i')
        sys.argv.append('w1g1')
        sys.argv.append('-f')
        sys.argv.append('-s')
        sys.argv.append('4')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK - 3/4 channels in OK state")


    def test_check3(self):
        """Test check3:
           -i w1g1 -f -s 4 -w 3 -c 1
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-i')
        sys.argv.append('w1g1')
        sys.argv.append('-f')
        sys.argv.append('-s')
        sys.argv.append('4')
        sys.argv.append('-w')
        sys.argv.append('3')
        sys.argv.append('-c')
        sys.argv.append('1')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 1)
            output = out.getvalue().strip()
            assert output.startswith("WARNING - 3/4 channels in OK state")

    def test_check4(self):
        """Test check4:
           -i w1g1 -f -s 4 -w 3 -c 3
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-i')
        sys.argv.append('w1g1')
        sys.argv.append('-f')
        sys.argv.append('-s')
        sys.argv.append('4')
        sys.argv.append('-w')
        sys.argv.append('3')
        sys.argv.append('-c')
        sys.argv.append('3')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL - 3/4 channels in OK state")


    def test_check5(self):
        """Test check5:
           -s 3
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-s')
        sys.argv.append('3')
        try:
            out = StringIO()
            sys.stdout = out
            check_wanpipe.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK - All of 3 channels are in OK state")




if __name__ == '__main__':
    unittest.main()
