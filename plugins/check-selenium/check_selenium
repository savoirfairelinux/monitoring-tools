#!/usr/bin/env python
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

# Copyright (C) 2014, Thibault Cohen <thibault.cohen@savoirfairelinux.com>

import unittest
import time
import re
import sys
import importlib
import os
from StringIO import StringIO

from shinkenplugins import BasePlugin, PerfData, STATES

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from xvfbwrapper import Xvfb


# Create a new class to get execution time
def make_testclass(super_class, parent):
    class testClassWithoutTimer(super_class):
        def __init__(self, *args, **kargs):
            self.parent = parent
            super(testClassWithoutTimer, self).__init__(*args, **kargs)

        def setUp(self):
            super(testClassWithoutTimer, self).setUp()
            # Get start time
            self.startTime = time.time()

        def tearDown(self):
            # Get end time
            self.parent.execution_time = time.time() - self.startTime
            super(testClassWithoutTimer, self).tearDown()
    return testClassWithoutTimer


class Plugin(BasePlugin):
    NAME = 'check-selenium'
    VERSION = '0.1'
    DESCRIPTION = 'Web tests using Selenium'
    AUTHOR = 'Thibault Cohen'
    EMAIL = 'thibault.cohen@savoirfairelinux.com'

    ARGS = [('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            ('w', 'warning', 'Warning threshold (seconds)', True),
            ('c', 'critical', 'Critical threshold (seconds)', True),
            ('W', 'width', 'Virtual display width', True),
            ('H', 'height', 'Virtual display height', True),
            ('d', 'debug', 'Launch firefox in the current display.'
                           'Usefull for scenario debuging', False),
            ('S', 'scenarios-folder', 'Scenarios folder', True),
            ('s', 'scenario-name', 'Scenario name to run', True),
            ('f', 'perfdata', 'Show perfdata', False),
            ]

    execution_time = None

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.

        # Mandatory arguments
        mandatory_arguments = ['scenarios-folder',
                               'scenario-name',
                               ]
        for argument_name in mandatory_arguments:
            if argument_name not in args:
                return False, 'the argument `%s is missing' % argument_name

        if args.get('scenario-name', None) is None:
            return False, 'The scenarios name must be set'

        # Check int arguments
        int_arguments = ['warning',
                         'critical',
                         ]
        for argument_name in int_arguments:
            if argument_name in args:
                try:
                    args[argument_name] = int(args[argument_name])
                except:
                    return False, "bad format: `%s'" % argument_name

        # Set default
        if 'perfdata' not in args:
            args['perfdata'] = False

        # Set default
        if 'debug' not in args:
            args['debug'] = False

        # Clean scenarios-folder
        if args['scenarios-folder'].endswith("/"):
            args['scenarios-folder'] = args['scenarios-folder'][:-1]

        # Check boolean
        bool_arguments = ['perfdata',
                          'debug',
                          ]
        for argument_name in bool_arguments:
            if args[argument_name] == '':
                args[argument_name] = True

        return True, None

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing
        # self.exit(return_code, 'return_message', *performance_data)
        scenario_name = args.get('scenario-name')
        scenario_folder = args.get('scenarios-folder')

        # Load scenario file
        if os.path.dirname(scenario_folder) not in sys.path:
            sys.path.append(os.path.dirname(scenario_folder))
        try:
            module = importlib.import_module("." + scenario_name,
                                             os.path.basename(scenario_folder))
        except:
            self.exit(STATES.UNKNOWN,
                      "UNKNOWN: Scenario '%s' not found in"
                      " %s" % (scenario_name, scenario_folder))

        # Prepare test
        test_case_module = getattr(module, scenario_name.capitalize())

        # Prepare StringIO to capture unittest output
        output = StringIO()
        # Init test runner
        self.ttr = unittest.TextTestRunner(stream=output)

        # Get tests
        suite = [unittest.defaultTestLoader.loadTestsFromTestCase(make_testclass(test_case_module, self))]
        testSuite = unittest.TestSuite(suite)

        # Start display
        if not args['debug']:
            vdisplay = Xvfb(width=1920, height=1080)
            vdisplay.start()

        # launch test
        try:
            result = self.ttr.run(testSuite)
        except Exception as exp:
            self.exit(STATES.UNKNOWN, "UNKNOWN: Error running test: %s" % exp)

        # Stop display
        if not args['debug']:
            vdisplay.stop()

        # Get execution test time
        self.execution_time = round(self.execution_time, 2)

        # Prepare output
        if not {'warning', 'critical'}.issubset(args):
            exit_code = STATES.OK
            message = ("OK: Scenario execution time: "
                       "%0.2f seconds" % self.execution_time)
        elif self.execution_time > args['critical']:
            exit_code = STATES.CRITICAL
            message = ("CRITICAL: Scenario execution time: "
                       "%0.2f seconds (> %0.2f)" % (self.execution_time,
                                                    args['critical']))
        elif self.execution_time > args['warning']:
            exit_code = STATES.WARNING
            message = ("WARNING: Scenario execution time: "
                       "%0.2f seconds (> %0.2f)" % (self.execution_time,
                                                    args['warning']))
        else:
            exit_code = STATES.OK
            message = ("OK: Scenario execution time: "
                       "%0.2f seconds" % self.execution_time)

        # Check fails and errors
        # Failures
        if len(result.failures) > 0:
            if args['debug']:
                message = str(result.failures[0][1])
            else:
                # We show only the first failure
                # And only the last line of its traceback
                message = "CRITICAL: " + \
                          result.failures[0][1].strip().split("\n")[-1]
            exit_code = STATES.CRITICAL
        # Errors
        if len(result.errors) > 0:
            if args['debug']:
                message = str(result.errors[0][1])
            else:
                # We show only the first error
                # And only the last line of its traceback
                error = result.errors[0][1].strip().split("\n")
                for line in error:
                    if line.find("Message:") != -1:
                        message = "CRITICAL: " + line
                        break
            exit_code = STATES.CRITICAL

        # Handle perfdata
        if args['perfdata']:
            # Set warning/critical
            if 'warning' not in args:
                args['warning'] = ''
            if 'critical' not in args:
                args['critical'] = ''
            # Add perfdata
            p1 = PerfData('time',
                          self.execution_time,
                          unit='s',
                          warn=args['warning'],
                          crit=args['critical'],
                          min_="0.0")
            # Exit
            self.exit(exit_code, message, p1)
        else:
            # Exit
            self.exit(exit_code, message)


if __name__ == "__main__":
    Plugin()
