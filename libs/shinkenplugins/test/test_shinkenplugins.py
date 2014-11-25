#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright (C) 2014 Savoir-Faire Linux Inc.
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

import unittest
import shinkenplugins


class TestShinkenPlugins(unittest.TestCase):

    def test_perfdata_none(self):
        perfdata = shinkenplugins.PerfData(
            'label',
            'value',
            unit=None,
            warn=None,
            crit=None,
            min_=None,
            max_=None,)

        self.assertEqual(perfdata.unit, '')
        self.assertEqual(perfdata.warn, '')
        self.assertEqual(perfdata.crit, '')
        self.assertEqual(perfdata.min_, '')
        self.assertEqual(perfdata.max_, '')
