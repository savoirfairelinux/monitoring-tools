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

import check_site_health

# the tests are expecting the output to be in plain english,
# so in case your env isn't in it let's force it:
os.environ['LANG'] = 'C'

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
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_site_health""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_site_health.py v%s"
                                     % check_site_health.PLUGIN_VERSION)

    def test_bad_arguments1(self):
        """Test bad arguments1:
           -H 127.0.0.1 -w toto
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('toto')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad format for WARNING argument")

    def test_bad_arguments2(self):
        """Test bad arguments2:
           -H 127.0.0.1 -f
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-f')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -f not recognized")

    def test_bad_arguments3(self):
        """Test bad arguments3:
           -H 127.0.0.1 -o 200 -w 404
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-o')
        sys.argv.append('200')
        sys.argv.append('-w')
        sys.argv.append('404')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("You can define OK option and WARNING/CRITICAL options")

    def test_bad_arguments4(self):
        """Test bad arguments4:
           -o 200,302
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-o')
        sys.argv.append('200,302')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Argument `hostname' is missing !")

    def test_bad_arguments5(self):
        """Test bad arguments5:
           -H 127.0.0.1 -c toto
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-c')
        sys.argv.append('toto')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad format for CRITICAL argument")

    def test_bad_arguments6(self):
        """Test bad arguments6:
           -H 127.0.0.1 -o toto
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-o')
        sys.argv.append('toto')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("Bad format for OK argument")

    def test_google_com1(self):
        """Test google.com1:
           -H google.com -c 404,500,501,502,503,504
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('google.com')
        sys.argv.append('-c')
        sys.argv.append('404,500,501,502,503,504')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK")

    def test_google_com2(self):
        """Test google.com2:
           -H google.com
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('google.com')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK")

    def test_sflphone_org(self):
        """Test sflphone.org (must have broken pages):
           -H sflphone.org
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('sflphone.org')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL")


    def test_bad_site(self):
        """Test bad_site.comd:
           -H bad_site.comd -o 200,302
        """ 
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('bad_site.comd')
        sys.argv.append('-o')
        sys.argv.append('200,302')
        try:
            out = StringIO()
            sys.stdout = out
            check_site_health.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL")


if __name__ == '__main__':
    unittest.main()
