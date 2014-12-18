# -*- coding: utf-8 -*-
"""
This is the module defining the ShinkenPlugin class.
"""

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
#   Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#############################################################################

from __future__ import unicode_literals, print_function, absolute_import

#############################################################################

import os
import re
import sys
import warnings

from traceback import format_exc

#############################################################################

from .version import __version__

#############################################################################

PY_VERSION = sys.version_info[:2]

try:
    import argparse
    from argparse import ArgumentParser
except ImportError:
    if PY_VERSION >= (2, 7):
        raise
    warnings.warn('argparse not available, using the one packaged within shinkenplugins')
    from . import argparse
    from .argparse import ArgumentParser


#############################################################################

from .states import STATES
from .states import STATES_2_NAME

#############################################################################

class PluginResult(object):
    def __init__(self, return_code, output, perf_datas=None):
        self.return_code = return_code
        self.output = output
        if perf_datas is None:
            perf_datas = []
        self.perf_datas = perf_datas

    def __repr__(self):
        return 'RC=%s output=%s n_perf_datas=%s' % (self.return_code, self.output, len(self.perf_datas))


class PluginResultException(SystemExit):
    ''' In order to be able to pass a plugin result along the original caller when
    it has been natively executed.

    This simply encapsulates an PluginResult instance in the result attribute.
    '''
    def __init__(self, result):
        self.result = result

#############################################################################

class PluginParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if status:
            status = STATES.UNKNOWN
        super(PluginParser, self).exit(status, message)

#############################################################################

class ShinkenPlugin(object):
    ''' Shinken Plugin.
    '''

    VERSION = 'unknown'
    DESCRIPTION = 'Check plugin'
    AUTHOR = 'nobody'
    EMAIL = 'nobody@nowhere'

    def __init__(self, progname=None, add_thresholds=False):
        if progname is None:
            progname = ( self.__class__.__name__ if isinstance(self, NativePlugin)
                         else sys.argv[0] )

        self.parser = PluginParser(progname, description=type(self).__doc__,
                                   version=self.version, epilog=self.support)
        if add_thresholds:
            self.add_warning_critical()

    #############################################################################

    def _make_threshold_dict(self, which):
        return {
            'type':     float,
            'help':     getattr(self, '_%s_help' % which, 'Set the %s threshold' % which)
        }

    def _add_threshold(self, which, kwargs=None):
        '''
        :param which: 'warning' | 'critical'
        :param kwargs: a dict to be given to parser.add_argument(**kwargs)
        '''
        self_kw = getattr(self, '_%s_kwargs' % which, {})
        kw = self._make_threshold_dict(which)
        kw.update(self_kw)
        if kwargs:
            kw.update(kwargs)
        if 'action' in kw: # if action was ever provided then remove our type one.
            del kw['type']
        self.parser.add_argument('-%s' % which[0], '--%s' % which, **kw)

    def add_warning_critical(self, warn_kw=None, crit_kw=None):
        self._add_threshold('warning', warn_kw)
        self._add_threshold('critical', crit_kw)

    #############################################################################

    def __str__(self):
        return '%s-%s' % (self.__class__.__name__, self.VERSION)

    def __repr__(self):
        return str(self)

    #############################################################################

    @property
    def version(self):
        return ('%s version %s (sfl-shinken-plugins)\n\n'
               'The SFL Shinken Plugins come with ABSOLUTELY NO WARRANTY. You may redistribute\n'
               'copies of the plugins under the terms of the GNU General Public License.\n'
               'For more information about these matters, see the file named COPYING.\n'
               % (self.NAME, self.VERSION))
    @property
    def support(self):
        return ('Send email to <{email}> if you have questions\n'
               'regarding use of this software. To submit patches or suggest improvements,\n'
               'send email to <{email}>\n'
               'Please include version information with all correspondence (when\n'
               'possible, use output from the --version option of the plugin itself).\n'.format(
                    email=self.EMAIL))

    #############################################################################

    def parse_args(self, args):
        return self.parser.parse_args(args)

    def run(self, args):
        raise NotImplementedError('You need to define the run(args) method within your plugin class.')

    def execute(self, orig_args=None):
        if orig_args is None:
            orig_args = sys.argv[1:]
        args = self.parse_args(orig_args)
        try:
            self.run(args)
        except Exception as err:
            traceback = format_exc()
            self.critical('''\
An unexpected error occurred: {err}
Please consider submitting a bug report to 'https://github.com/savoirfairelinux/monitoring-tools/issues' \
with all the following data attached:
=============================================================================
<<< BEGIN BUG DATA
-----------------------------------------------------------------------------
Plugin={self.NAME} Version={self.VERSION}
shinkenpluginVersion={version}
OriginalArguments={orig_args}
ParsedArguments={args}
PythonVersion={sys.version_info}
-----------------------------------------------------------------------------
{traceback}
-----------------------------------------------------------------------------
<<< END BUG DATA
=============================================================================
'''.format(self=self, sys=sys, version=__version__, err=err,
           args=args, orig_args=orig_args, traceback=traceback))
        else:
            self.ok('Service succeeded')

    #############################################################################

    def exit(self, return_code, message, *perfdata):
        if __debug__:
            if return_code not in (0, 1, 2, 3):
                warnings.warn('Invalid return_code value: %r ; forcing to UNKNOWN ..')
                return_code = STATES.UNKNOWN
            if '|' in message:
                warnings.warn("Plugin output message contains the '|' character, which is forbidden !\n"
                              "Please give perfdata as parameters.")

        s_perf = '' if not perfdata else "|%s" % (' '.join(str(pd) for pd in perfdata))
        print('%(level)s: %(message)s%(perf)s' % {
                'level':  STATES_2_NAME.get(return_code, 'UNKNOWN'),
                'message': message,
                'perf': s_perf})
        sys.exit(return_code)

    #############################################################################

    ## all 4 following functions could also certainly be factorized somehow..
    def ok(self, message, *perfdata):
        self.exit(STATES.OK, message, *perfdata)

    def unknown(self, message, *perfdata):
        self.exit(STATES.UNKNOWN, message, *perfdata)

    def warning(self, message, *perfdata):
        self.exit(STATES.WARNING, message, *perfdata)

    def critical(self, message, *perfdata):
        self.exit(STATES.CRITICAL, message, *perfdata)


#############################################################################

class NativePlugin(ShinkenPlugin):
    ''' Designed to be "directly" executed by Shinken poller. Without a supplementary fork.
    For doing so this specialized plugin will simply return, from its execute method,
    the results as a PluginResult instance.
    '''

    def exit(self, return_code, message, *perf_datas):
        result = PluginResult(return_code, message, perf_datas)
        raise PluginResultException(result)

    def execute(self, orig_args):
        try:
            super(NativePlugin, self).execute(orig_args)
            # if one doesn't use our execute method and doesn't call any of ok/warning/critical/unknown
            # then we'll fall here..
            # still consider this as a success though it could be tricky/risky..
            warnings.warn("%s doesn't explicitly call any of ok/warning/critical/unknown, assuming success" % self)
            self.ok('%s succeeded' % self)
        except PluginResultException as res:
            return res.result

