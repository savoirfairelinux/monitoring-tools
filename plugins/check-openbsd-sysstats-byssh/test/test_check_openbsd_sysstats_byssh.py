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

import check_openbsd_sysstats_byssh


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
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_openbsd_sysstats_byssh""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_openbsd_sysstats_byssh.py v%s"
                                     % check_openbsd_sysstats_byssh.PLUGIN_VERSION)

    def test_badarguments1(self):
        """Test test_badarguments1:
            -H 192.168.1.1 -d
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.1.1')
        sys.argv.append('-d')
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -d not recognized")

    def test_badarguments2(self):
        """Test test_badarguments2:
            -H 192.168.1.1 --load-warning 0,3,6
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.1.1')
        sys.argv.append('--load-warning')
        sys.argv.append('0,3,6')
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Warning and Critical ")

    def test_badarguments3(self):
        """Test test_badarguments3:
            -H 192.168.1.1 -d
        """
        sys.argv = [sys.argv[0]]
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Argument `hostname' is missing !")

    def test_badarguments2(self):
        """Test test_badarguments2:
            -H 192.168.1.1 --load-warning 0,3,6 --load-critical 4.5,6
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.1.1')
        sys.argv.append('--load-warning')
        sys.argv.append('0,3,6')
        sys.argv.append('--load-critical')
        sys.argv.append('4.5,6')
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad format:")

    def test_check1(self):
        """Test check1:
            -H 192.168.1.1
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.1.1')
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK - ")

    def test_check2(self):
        """Test check2:
            -H 192.168.1.1
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('192.168.1.1')
        sys.argv.append('--load-warning')
        sys.argv.append('0,3,6')
        sys.argv.append('--load-critical')
        sys.argv.append('5,7,9')
        try:
            out = StringIO()
            sys.stdout = out
            check_openbsd_sysstats_byssh.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 1)
            output = out.getvalue().strip()
            assert output.startswith("WARNING - ")


if __name__ == '__main__':
    unittest.main()
