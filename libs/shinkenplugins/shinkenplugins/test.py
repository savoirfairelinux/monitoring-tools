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
from shinkenplugins.plugin import ShinkenPlugin


class TestPlugin(unittest.TestCase, object):
    """
    A class to test plugin inputs/outputs.
    """
    def execute(self, plugin, args, return_value, stdout_pattern='', debug=False, stderr_pattern=''):
        sys.argv = [sys.argv[0]]
        for arg in args:
            sys.argv.append(arg)

        new_out = StringIO()
        new_err = StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = new_out
        sys.stderr = new_err
        
        with self.assertRaises(SystemExit) as context:
            try:
                plug = plugin()
                if issubclass(plugin, ShinkenPlugin):
                    plug.execute()
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        stdout_output = new_out.getvalue().strip()
        stderr_output = new_err.getvalue().strip()

        err = context.exception
        if debug:
            print('Expected: %d, received: %d' % (return_value, err.code))
            print('Expected output: %s, received: %s' % (stdout_pattern, stdout_output))

        self.assertEquals(err.code, return_value, 'stdout=%r stderr=%r' % (stdout_output, stderr_output))
        self.assertRegexpMatches(stdout_output, stdout_pattern)
        self.assertRegexpMatches(stderr_output, stderr_pattern)
        # in python >= 3.2 : change me to assertRegex
        # see: https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertRegex
