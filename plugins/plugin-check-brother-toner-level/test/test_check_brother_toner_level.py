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

import check_brother_toner_level


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
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_brother_toner_level""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_brother_toner_level.py v%s"
                                     % check_brother_toner_level.PLUGIN_VERSION)

    def test_get_data_pages1(self):
        """Test get data:
           -H 127.0.0.1:51511 -n Black
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1:51511')
        sys.argv.append('-n')
        sys.argv.append('Black')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL: Toner Black")

    def test_get_data_pages2(self):
        """Test get data2:
           -H 127.0.0.1:51512
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1:51512')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("All consumables are OK")


    def test_get_data_pages3(self):
        """Test get data3:
           -H 127.0.0.1:51512
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1:51512')
        sys.argv.append('-s')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.find("Drum Unit Cyan (C)") != -1
            assert output.find("Drum Unit Yellow (Y)") != -1
            assert output.find("Toner Yellow (Y)") != -1
            assert output.find("Fuser Unit:") != -1

    def test_bad_arguments1(self):
        """Test bad arguments1:
           -H 127.0.0.1:51512 -g
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1:51512')
        sys.argv.append('-g')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -g not recognized")

    def test_bad_arguments2(self):
        """Test bad arguments2:
        """
        sys.argv = [sys.argv[0]]
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Argument `hostname' is missing")

    def test_bad_arguments3(self):
        """Test bad arguments3:
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('1.1.1.1')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.find("HTTP request timeout") != -1

    def test_bad_arguments4(self):
        """Test bad arguments4:
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('20')
        sys.argv.append('-c')
        sys.argv.append('30')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Warning threshold must be greater than Critical")

    def test_no_consomables_found(self):
        """Test no consumables found:
           -H 127.0.0.1:51511 -n Blackasdg
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1:51511')
        sys.argv.append('-n')
        sys.argv.append('Blackasdg')
        try:
            out = StringIO()
            sys.stdout = out
            check_brother_toner_level.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("No consumables found...")


if __name__ == '__main__':
    unittest.main()
