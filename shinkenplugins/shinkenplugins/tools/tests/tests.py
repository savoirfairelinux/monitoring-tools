#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#  Author: Grégory Starck gregory.starck@savoirfairelinux.com
#
#

import sys
import unittest
from StringIO import StringIO


class TestPluginBase(unittest.TestCase):
    ''' Simple class to help at testing a plugin. '''

    def do_tst(self, return_val, pattern_to_search, main=None):
        main = main or self._main
        prev_out = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            main()
        except SystemExit as err:
            output = out.getvalue().strip()
            self.assertEquals(err.code, return_val,
                              'Return code does not match expected one: '
                              'received=%s, expected=%s' % (err.code, return_val))
            self.assertRegexpMatches(output, pattern_to_search)
        finally:
            sys.stdout = prev_out
