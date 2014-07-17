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
# Authors:  Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
#           Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>


import sys
import re
import getopt
import itertools
import unittest
from collections import namedtuple
from StringIO import StringIO

def get_states_tuple():
    """
    Returns a namedtuple used to keep human-readable values of all
    the different return states.
    """
    States = namedtuple('States', 'OK, WARNING, CRITICAL, UNKNOWN')
    STATES = States(0, 1, 2, 3)
    return STATES
STATES = get_states_tuple()

class PerfData(object):
    """
    An object holding a plugin performance data, and whose string
    representation matches the one needed in a plugin output.
    """
    def __init__(self, label, value, unit='', warn='', crit='', min='', max=''):
        self.__dict__.update(locals())
    
    def __repr__(self):
        return ('%(label)s=%(value)s%(unit)s;%(warn)s;%(crit)s;%(min)s;%(max)s'
                % self.__dict__)

class BasePlugin(object):
    """
    A simple plugin.
    Manages the metadata, input (arguments) and output.
    """
    def __init__(self):
        args = self.get_args()
        
        if 'help' in args.keys():
            self.version()
            self.usage()
            self.support()
            self.exit(STATES.UNKNOWN, '')
        if 'version' in args.keys():
            self.version()
            self.support()
            self.exit(STATES.UNKNOWN, '')
        
        check = self.check_args(args)
        if not check[0]:
            print('Arguments error: %s' % str(check[1]))
            self.usage()
            self.exit(STATES.UNKNOWN, '')

        self.run(args)

    def check_args(self, args):
        return True, None

    def get_args(self):
        expected = self.__class__.ARGS
        getopt_magicstr = ''.join(itertools.chain.from_iterable([[x[0], ':' if x[3] else '']
                                                                 for x in expected]))
        getopt_longargs = [''.join([x[1], '=' if x[3] else '']) for x in expected]

        try:
            options, args = getopt.getopt(sys.argv[1:],
                                          getopt_magicstr,
                                          getopt_longargs)
        except getopt.GetoptError, err:
            print str(err)
            self.usage()
            sys.exit(STATES.UNKNOWN)

        args = {}
        short_args = ['-' + x[0] for x in expected]
        long_args = ['--' + x[1] for x in expected]
        
        for option_name, value in options:
            for (short, long_) in zip(short_args, long_args):
                if option_name in (short, long_):
                    args[long_[2:]] = value
        return args

    def version(self):
        version_msg = ('%s version %s (sfl-shinken-plugins)\n\n'
                       'The SFL Shinken Plugins come with ABSOLUTELY NO WARRANTY. You may redistribute\n'
                       'copies of the plugins under the terms of the GNU General Public License.\n'
                       'For more information about these matters, see the file named COPYING.\n'
                       % (self.__class__.NAME, self.__class__.VERSION))
        print(version_msg)
    
    def support(self):
        support_msg = ('Send email to <%s> if you have questions\n'
                       'regarding use of this software. To submit patches or suggest improvements,\n'
                       'send email to <%s>\n'
                       'Please include version information with all correspondence (when\n'
                       'possible, use output from the --version option of the plugin itself).\n'
                       % (self.__class__.EMAIL, self.__class__.EMAIL))
        print(support_msg)
    
    def usage(self):
        args = self.__class__.ARGS
        short = ''
        long_ = ''
        for arg in args:
            # adds '=FOO' for arguments which expect a value
            s_expected = ' <' + arg[1] + '>' if arg[3] else ''
            l_expected = '=' + arg[1].upper() if arg[3] else ''
            short += ' -' + arg[0] + s_expected
            long_ += ' --' + arg[0] + ', --' + arg[1] + l_expected + '\n    ' + arg[2] + '\n'

        print('%s %s' % (self.__class__.NAME, short))
        print('')
        print('Usage:')
        print(long_)

    def run(self, args):
        raise NotImplementedError('You need to define the run() method with '
                                  'the core of your plugin.')

    def exit(self, return_code, message, *perfdata):
        if perfdata:
            print('%(message)s|%(perfs)s' % {'message': message,
                                            'perfs': ' '.join([str(x) for x in perfdata])})
        else:
            print('%s' % message)
        sys.exit(return_code)

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
            plugin()
        except SystemExit, e:
            sys.stdout = old_stdout
            output = out.getvalue().strip()
            
            if debug:
                print('Expected: %d, received: %d' % (return_value, e.code))
                print('Expected output: %s, received: %s' % (pattern, output))
                
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, return_value)
            self.assertTrue(re.search(pattern, output))
