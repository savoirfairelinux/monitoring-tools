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

import re
import sys
import unittest
from StringIO import StringIO


class TestPluginBase(unittest.TestCase):

    def do_tst(self, return_val, pattern_to_search, main=None):
        main = main or self._main
        try:
            out = StringIO()
            prev_out = sys.stdout
            sys.stdout = out
            main()
        except SystemExit as err:
            output = out.getvalue().strip()
            self.assertEquals(err.code, return_val)
            matches = re.search(pattern_to_search, output)
            assert matches is not None
        finally:
            sys.stdout = prev_out
