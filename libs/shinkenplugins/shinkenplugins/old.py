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

import sys
import getopt
import itertools

from traceback import format_exc
from collections import namedtuple

#############################################################################

from .version import __version__

#############################################################################

from .states import STATES

#############################################################################

class BasePlugin(object):
    """
    A simple plugin.
    Manages the metadata, input (arguments) and output.
    """
    def __init__(self, args=None):
        if args is None:
            args = sys.argv[1:]
        self._orig_args = args
        args = self.get_args(args)

        if 'help' in args.keys():
            self.usage(self.version, post_msg=self.support)

        if 'version' in args.keys():
            self.usage(self.version + '\n' + self.support)

        check = self.check_args(args)
        if not check[0]:
            self.usage('Arguments error: %s' % str(check[1]))

        self.execute_run(args)

    def execute_run(self, args):
        try:
            self.run(args)
        except Exception as err:
            traceback = format_exc()
            sys_ = sys
            version = __version__
            self.critical('''\
An unexpected error occurred: {err}
Please consider submitting a bug report to 'https://github.com/savoirfairelinux/monitoring-tools/issues' \
with all the following data attached:
=============================================================================
<<< BEGIN BUG DATA
-----------------------------------------------------------------------------
Plugin={self.NAME} Version={self.VERSION}
shinkenpluginVersion={version}
OriginalArguments={self._orig_args}
ParsedArguments={args}
PythonVersion={sys_.version_info}
-----------------------------------------------------------------------------
{traceback}
-----------------------------------------------------------------------------
<<< END BUG DATA
=============================================================================
'''.format(**locals()))

    def check_args(self, args):
        return True, None

    def get_args(self, args):
        expected = self.ARGS
        getopt_magicstr = ''.join(itertools.chain.from_iterable([[x[0], ':' if x[3] else '']
                                                                 for x in expected]))
        getopt_longargs = [''.join([x[1], '=' if x[3] else '']) for x in expected]

        try:
            options, args = getopt.getopt(args,
                                          getopt_magicstr,
                                          getopt_longargs)
        except getopt.GetoptError as err:
            print(err)
            self.usage()

        args = {}
        short_args = ['-' + x[0] for x in expected]
        long_args = ['--' + x[1] for x in expected]

        for option_name, value in options:
            for (short, long_) in zip(short_args, long_args):
                if option_name in (short, long_):
                    args[long_[2:]] = value
        return args

    @property
    def version(self):
        return ('%s version %s (sfl-shinken-plugins)\n\n'
               'The SFL Shinken Plugins come with ABSOLUTELY NO WARRANTY. You may redistribute\n'
               'copies of the plugins under the terms of the GNU General Public License.\n'
               'For more information about these matters, see the file named COPYING.\n'
               % (self.NAME, self.VERSION))
    @property
    def support(self):
        return ('Send email to <%s> if you have questions\n'
               'regarding use of this software. To submit patches or suggest improvements,\n'
               'send email to <%s>\n'
               'Please include version information with all correspondence (when\n'
               'possible, use output from the --version option of the plugin itself).\n'
               % (self.EMAIL, self.EMAIL))

    def usage(self, pre_msg=None, post_msg=None, exit_code=STATES.UNKNOWN):
        if pre_msg:
            print(pre_msg)
        args = self.ARGS
        short = ''
        long_ = ''
        for arg in args:
            # adds '=FOO' for arguments which expect a value
            s_expected = ' <' + arg[1] + '>' if arg[3] else ''
            l_expected = '=' + arg[1].upper() if arg[3] else ''
            short += ' -' + arg[0] + s_expected
            long_ += ' -' + arg[0] + ', --' + arg[1] + l_expected + '\n    ' + arg[2] + '\n'

        print('%s %s' % (self.NAME, short))
        print('')
        print('Usage:')
        print(long_)
        if post_msg:
            print(post_msg)
        if exit_code is not None:
            sys.exit(exit_code)

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

    ## all 4 following functions could also certainly be factorized somehow..
    def ok(self, message, *perfdata):
        self.exit(STATES.OK, message, *perfdata)

    def unknown(self, message, *perfdata):
        self.exit(STATES.UNKNOWN, message, *perfdata)

    def warning(self, message, *perfdata):
        self.exit(STATES.WARNING, message, *perfdata)

    def critical(self, message, *perfdata):
        self.exit(STATES.CRITICAL, message, *perfdata)
