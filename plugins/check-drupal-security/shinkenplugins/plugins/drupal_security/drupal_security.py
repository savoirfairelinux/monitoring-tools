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

# Copyright (C) 2014, vdnguyen <vanduc.nguyen@savoirfairelinux.com>
# 2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import
import json
import subprocess

from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.states import STATES


class CheckDrupalSecurity(ShinkenPlugin):
    NAME = 'drupal_security'
    VERSION = '1.0'
    DESCRIPTION = 'A plugin to monitor Drupal security'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'

    def __init__(self):
        super(CheckDrupalSecurity, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('-p', '--drupal-path', required=False,
                                 help='Drupal installation path for local'
                                      ' drush'),
        self.parser.add_argument('-a', '--alias', required=False,
                                 help='Alias to use for remote drush'),
        self.parser.add_argument('-d', '--home-dir', required=False,
                                 help='Home directory where the .drush '
                                      'containing the alias config can '
                                      'be found')

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckDrupalSecurity, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        if args.alias is None and args.drupal_path is None:
            self.parser.error('Either --alias and --home-dir '
                              'or --drupal-path must be set')
        if (args.alias is None and args.home_dir is not None) or \
           (args.alias is not None and args.home_dir is None):
            self.parser.error('--home-dir must be used with --alias')
        if args.alias is not None and args.drupal_path is not None:
            self.parser.error('--alias and --drupal-path can\'t be both set')

        return args

    def _get_site_audit_result(self):
        try:
            if self.alias is not None:
                args = [self.alias, '--json', 'asec']
                data = self._call_site_audit(args)
                data = self._extract_json_from_output(data)
            else:
                args = ['--json', 'asec']
                data = self._call_site_audit(args)

            data = json.loads(data)
        except subprocess.CalledProcessError, e:
            return None, "Command 'drush " + ' '.join(args) + "' " \
                         "returned non-zero exit status 1"
        except OSError, e:
            return None, e.strerror
        except NoJsonFoundError, e:
            return None, e.message
        return data, None

    def _call_site_audit(self, args):
        cmd = ['drush'] + args

        with open('/dev/null', 'w') as devnull:
            out = subprocess.check_output(cmd,
                                          cwd=self.path,
                                          stderr=devnull,
                                          env={'HOME': self.home})
        return out

    def _extract_json_from_output(self, output):
        """ Used to extract a JSON from the dirty remote drush output """
        json_beg = output.find('{')
        json_end = output.rfind('}') + 1
        same_line = False

        # Make sure that the opening curly bracket is on the same line as the
        # closing one.
        while not same_line:
            if json_beg == -1:
                raise NoJsonFoundError('No JSON found in the output')
            elif json_end <= output.find('\n', json_beg):
                same_line = True
            else:
                json_beg = output.find('{', json_beg, json_end)

        return output[json_beg:json_end]

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        self.alias = args.alias
        self.path = args.drupal_path
        self.home = args.home_dir

        data, e_msg = self._get_site_audit_result()

        if data is None:
            self.unknown(e_msg)

        status = data['percent']
        message = []
        score_format = '%.2f%%\n'

        if status <= args.critical:
            message.append(score_format % status)
            code = STATES.CRITICAL
        elif status <= args.warning:
            message.append(score_format % status)
            code = STATES.WARNING
        else:
            message.append(score_format % status)
            code = STATES.OK

        action = data['checks']['SiteAuditCheckSecurityMenuRouter']['action']
        action = action if action is not None else ''

        message.append(
            '%s;%d;%s;' % (
                data['checks']['SiteAuditCheckSecurityMenuRouter']['result'],
                data['checks']['SiteAuditCheckSecurityMenuRouter']['score'],
                action
            )
        )

        self.exit(code, ''.join(message))


class NoJsonFoundError(Exception):
    pass


############################################################################

Plugin = CheckDrupalSecurity

############################################################################


def main(argv=None):
    plugin = CheckDrupalSecurity()
    plugin.execute(argv)


if __name__ == "__main__":
    main()