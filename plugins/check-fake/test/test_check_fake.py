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
#            test_check_fake
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

import check_fake


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
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""check_fake """)

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("check_fake v%s"
                                     % check_fake.PLUGIN_VERSION)

    def test_missing_args(self):
        """Test missings args:
           -S apache -t TEXT
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-S')
        sys.argv.append('apache1')
        sys.argv.append('-t')
        sys.argv.append('TEXT')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("""Argument `hostname' is missing !""")

    def test_bad_argument(self):
        """Test bad args :
           -H webserver -S apache -t INT64 -l 0 -s 0 -e 5
           -H webserver -S apache -t INT64 -l 0 -s 6 -e 2
           -H webserver -S apache -t INT -l 0 -s 0 -e 2
           -H webserver -S apache -g INT64 -l 1 -s 0 -e 2
        """
        # -H webserver -S apache -t INT64 -l 0 -s 0 -e 5
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache')
        sys.argv.append('-t')
        sys.argv.append('INT64')
        sys.argv.append('-l')
        sys.argv.append('0')
        sys.argv.append('-s')
        sys.argv.append('0')
        sys.argv.append('-e')
        sys.argv.append('5')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output == """Error state must be 0, 1, 2 or 3"""

        # -H webserver -S apache -t INT64 -l 0 -s 6 -e 2
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache')
        sys.argv.append('-t')
        sys.argv.append('INT64')
        sys.argv.append('-l')
        sys.argv.append('0')
        sys.argv.append('-s')
        sys.argv.append('6')
        sys.argv.append('-e')
        sys.argv.append('2')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output == """State must be 0, 1, 2 or 3"""

        # -H webserver -S apache -t INT -l 0 -s 0 -e 2
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache')
        sys.argv.append('-t')
        sys.argv.append('INT')
        sys.argv.append('-l')
        sys.argv.append('0')
        sys.argv.append('-s')
        sys.argv.append('0')
        sys.argv.append('-e')
        sys.argv.append('2')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output == "Type must be INT64, INT32, INT16, TEXT or BOOL"

        # -H webserver -S apache -g INT64 -l 0 -s 0 -e 2
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache')
        sys.argv.append('-g')
        sys.argv.append('INT64')
        sys.argv.append('-l')
        sys.argv.append('0')
        sys.argv.append('-s')
        sys.argv.append('0')
        sys.argv.append('-e')
        sys.argv.append('2')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 3)
            output = out.getvalue().strip()
            assert output.startswith("option -g not recognized")

    def test_default_args(self):
        """Test default values:
           -H webserver -S apache -t TEXT
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache1')
        sys.argv.append('-t')
        sys.argv.append('TEXT')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)

    def test_ok_return(self):
        """Test plugin with the following args :
           -H webserver -S apache -t INT64 -l 0 -s 0 -e 1
        """
        check_fake.POOL_FOLDER = "/fake_folder"
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache1')
        sys.argv.append('-t')
        sys.argv.append('INT64')
        sys.argv.append('-l')
        sys.argv.append('0')
        sys.argv.append('-s')
        sys.argv.append('0')
        sys.argv.append('-e')
        sys.argv.append('1')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 0)
            output = out.getvalue().strip()
            assert output.startswith("OK: ")

    def test_error_return(self):
        """Test plugin with the following args :
           -H webserver -S apache -t INT64 -l 0 -s 0 -e 1
        """
        f = open("/tmp/webserver_apache", "w")
        f.close()
        check_fake.POOL_FOLDER = "/tmp"
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('webserver')
        sys.argv.append('-S')
        sys.argv.append('apache')
        sys.argv.append('-t')
        sys.argv.append('INT16')
        sys.argv.append('-l')
        sys.argv.append('0')
        sys.argv.append('-s')
        sys.argv.append('0')
        sys.argv.append('-e')
        sys.argv.append('2')
        try:
            out = StringIO()
            sys.stdout = out
            check_fake.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
            output = out.getvalue().strip()
            assert output.startswith("CRITICAL: ")


if __name__ == '__main__':
    unittest.main()
