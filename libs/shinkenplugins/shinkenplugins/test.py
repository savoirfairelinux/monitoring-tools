# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2014, Savoir-faire Linux, Inc.
# Authors:
#   Grégory Starck <gregory.starck@savoirfairelinux.com>
#   Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
#   Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#############################################################################

from __future__ import unicode_literals, print_function, absolute_import

#############################################################################

import sys
import unittest
from StringIO import StringIO


class TestPlugin(unittest.TestCase):
    """
    A class to test plugin inputs/outputs.
    """
    def execute(self, plugin, args, return_value, pattern, debug=False):
        sys.argv = [sys.argv[0]]
        for arg in args:
            sys.argv.append(arg)

        out = StringIO()
        old_stdout = sys.stdout
        sys.stdout = out
        
        try:
            try:
                plugin()
            finally:
                sys.stdout = old_stdout
        except SystemExit as err:
            output = out.getvalue().strip()
            
            if debug:
                print('Expected: %d, received: %d' % (return_value, err.code))
                print('Expected output: %s, received: %s' % (pattern, output))

            self.assertEquals(err.code, return_value, output)
            self.assertRegexpMatches(output, pattern)
            # in python >= 3.2 : change me to assertRegex
            # see: https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertRegex
