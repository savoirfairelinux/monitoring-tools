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
#            check_printer_hp_2600n Check toner level from a hp 2600n printer
#
#
#  Author: Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import unittest
import sys
#import os
import re
from StringIO import StringIO

sys.path.append("..")

import check_printer_hp_2600n


class TestPlugin(unittest.TestCase):
    def setUp(self):
        pass

    def test_help(self):
        """Test help output :
           -h
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-h')
        self.do_tst(3, """^check_printer_hp_2600n""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        self.do_tst(3, "^check_printer_hp_2600n.py v%s" % check_printer_hp_2600n.PLUGIN_VERSION)

    def do_tst(self, return_val, pattern_to_search):
        try:
            out = StringIO()
            sys.stdout = out
            check_printer_hp_2600n.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, return_val)
            output = out.getvalue().strip()
            matches = re.search(pattern_to_search, output)
            assert matches is not None

    def test_base(self):
        """Test test_base :
        -H 127.0.0.1 -P 51515 -w 20 -c 10
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('20')
        sys.argv.append('-c')
        sys.argv.append('10')
        sys.argv.append('-P')
        sys.argv.append('51515')
        self.do_tst(0, "^OK # Toners OK")

    def test_color_good(self):
        """Test test_color_good :
        -H 127.0.0.1 -P 51515 -w 20 -c 10 -C CYAN
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('20')
        sys.argv.append('-c')
        sys.argv.append('10')
        sys.argv.append('-C')
        sys.argv.append('CYAN')
        sys.argv.append('-P')
        sys.argv.append('51515')

        self.do_tst(0, "^OK # Toners OK")

    def test_color_bad(self):
        """Test test_color_bad :
        -H 127.0.0.1 -P 51515 -w 20 -c 10 -C QSDF
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('20')
        sys.argv.append('-c')
        sys.argv.append('10')
        sys.argv.append('-C')
        sys.argv.append('QSDF')
        sys.argv.append('-P')
        sys.argv.append('51515')
        self.do_tst(3, "UNKNOWN - Color QSDF not in found data collected")

    def test_default_val(self):
        """Test test_default_val :
        -H 127.0.0.1 -P 51515 -w 20 -c 10 -P 80 -p device_status_info.htm
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('20')
        sys.argv.append('-c')
        sys.argv.append('10')
        sys.argv.append('-P')
        sys.argv.append('51515')
        sys.argv.append('-p')
        sys.argv.append('/SSI/device_status_info.htm')
        self.do_tst(0, "^OK # Toners OK")

    def test_missing_args(self):
        """Test test_missing_args :
        -H 127.0.0.1
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        self.do_tst(3, "UNKNOWN - Argument .* missing")

    def test_bad_warning_val(self):
        """Test test_bad_warning_val :
        -H 127.0.0.1 -w 10 -c 20
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('10')
        sys.argv.append('-c')
        sys.argv.append('20')
        self.do_tst(3, "^UNKNOWN - Wrong warning or critical values. Please ensure warning > critical")

    def test_bad_page(self):
        """Test test_bad_page :
        -H 127.0.0.1 -P 51515 -w 10 -c 5 -p QSDQSD
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-P')
        sys.argv.append('51515')
        sys.argv.append('-w')
        sys.argv.append('10')
        sys.argv.append('-c')
        sys.argv.append('5')
        sys.argv.append('-p')
        sys.argv.append('QSDQSD')
        self.do_tst(2, "^CRITICAL - Can't get data from the device")

    def test_bad_opt(self):
        """Test test_bad_opt :
        -K
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-K')
        self.do_tst(3, "^option -. not recognized")

    def test_warning_out(self):
        """Test test_warning_out :
        -H 127.0.0.1 -w 100 -c 10 -P 51515
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('100')
        sys.argv.append('-c')
        sys.argv.append('10')
        sys.argv.append('-P')
        sys.argv.append('51515')
        self.do_tst(1, "^WARNING #")

    def test_critical_out(self):
        """Test test_critical_out :
        -H 127.0.0.1 -w 100 -c 100 -P 51515
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('100')
        sys.argv.append('-c')
        sys.argv.append('100')
        sys.argv.append('-P')
        sys.argv.append('51515')
        self.do_tst(2, "^CRITICAL #")

    def test_bad_port(self):
        """Test test_bad_port :
        -H 127.0.0.1 -P 11111
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-H')
        sys.argv.append('127.0.0.1')
        sys.argv.append('-w')
        sys.argv.append('10')
        sys.argv.append('-c')
        sys.argv.append('5')
        sys.argv.append('-P')
        sys.argv.append('11111')
        self.do_tst(2, "^CRITICAL -")

if __name__ == '__main__':
    unittest.main()
