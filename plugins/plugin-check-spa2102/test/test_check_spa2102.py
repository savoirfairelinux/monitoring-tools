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
#            check_spa2102 Check Linksys SPA-2102 status
#
#
#  Author: Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import unittest
import sys
#import os
from StringIO import StringIO

sys.path.append("..")

import check_spa2102


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
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_spa2102""")

    def test_empty(self):
        """Test empty :

        """
        sys.argv = [sys.argv[0]]
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("UNKNOWN - Argument '")

    def test_bad_arg(self):
        """Test bad_arg :

        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-K')
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option")

    def test_default(self):
        """Test default :

        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL - Can't connect to")

    def test_bad_line(self):
        """Test bad_line :

        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-l')
        sys.argv.append('3')
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("UNKNOWN - Bad number for the line parameter line")

    def test_first_line(self):
        """Test first line :
           -H 127.0.0.1 -P 51515 -p /spa-2102.htm -l 1
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-P')
        sys.argv.append('51515')
        sys.argv.append('-p')
        sys.argv.append('/spa-2102.htm')
        sys.argv.append('-l')
        sys.argv.append('1')
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK - Line")

    def test_second_line(self):
        """Test second line :
           -H 127.0.0.1 -P 51515 -p /spa-2102.htm -l 2
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-P')
        sys.argv.append('51515')
        sys.argv.append('-p')
        sys.argv.append('/spa-2102.htm')
        sys.argv.append('-l')
        sys.argv.append('2')
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL - Line")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_spa2102.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_spa2102.py v%s"
                                     % check_spa2102.PLUGIN_VERSION)


if __name__ == '__main__':
    unittest.main()
