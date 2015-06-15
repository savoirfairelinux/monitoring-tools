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
import re
import subprocess

from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.states import STATES


class CheckDrupalStatus(ShinkenPlugin):
    NAME = 'drupal_status'
    VERSION = '1.0'
    DESCRIPTION = 'A plugin to monitor Drupal status'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'

    def __init__(self):
        super(CheckDrupalStatus, self).__init__()
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
        args = super(CheckDrupalStatus, self).parse_args(args)
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

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        self.path = args.drupal_path
        self.home = args.home_dir

        cmd1 = ['--json', '--detail', 'as']
        cmd2 = ['ups', '--format=csv']

        if args.alias:
            cmd1 = [args.alias] + cmd1
            cmd2 = [args.alias] + cmd2

        data, e_msg = self._get_drush_result(cmd1)
        update_status, e_msg = self._get_drush_result(cmd2)

        if data is None or e_msg is not None:
            self.unknown(e_msg)

        if args.alias:
            try:
                data = self._extract_json_from_output(data)
            except NoJsonFoundError, e:
                self.exit(STATES.UNKNOWN, e.message)
            update_status = self._extract_csv_from_output(update_status)
        else:
            update_status = update_status.strip().split('\n')

        data = json.loads(data)
        info = data['checks']['SiteAuditCheckStatusSystem']['result']
        info = info.split('\n')
        info = {line.split(':')[0]: line.split(':')[1] for line in info}

        if len(update_status) == 1 and update_status[0].strip() == '':
            update_status = []
        else:
            update_status = [(update.split(',')[0], update.split(',')[3])
                             for update in update_status]

        result = []

        result.append(
            ('Drupal Core version',
             info['Drupal'].split('-')[1].strip(),
             -1)
        )
        result.append(
            ('Database system',
             info['Database system'].split('-')[1].strip(),
             -1)
        )
        result.append(
            ('DBMS version',
             info['Database system version'].split('-')[1].strip(),
             -1)
        )
        result.append(
            ('Database update',
             info['Database updates'].split('-')[1].strip(),
             -1)
        )
        result.append(
            ('PHP version',
             info['PHP'].split('-')[1].strip().split(' ')[0],
             -1)
        )

        code = STATES.OK
        msg = 'Everything is up to date'

        # To maintain consistency between Drupal plugins, site_audit's levels
        # are used. So, level -1 = info, 0 = critical, 1 = warning and 2 = OK
        for (mod_name, mod_status) in update_status:
            mod_status = mod_status.strip()
            if mod_status == 'Up to date':
                level = 2
            elif mod_status == 'Update available':
                if code < 1:
                    code = STATES.WARNING
                    msg = 'Updates available'
                level = 1
            elif mod_status == 'SECURITY UPDATE available':
                if code < 2:
                    code = STATES.CRITICAL
                    msg = 'SECURITY UPDATE available'
                level = 0
            else:
                level = -1

            result.append((mod_name, mod_status, level))

        out = [msg]

        for (key, value, level) in result:
            out.append("%s;%s;%d" % (key, value, level))

        self.exit(code, '\n'.join(out))

    def _get_drush_result(self, cmd):
        try:
            data = self._call_site_audit(cmd)
        except subprocess.CalledProcessError, e:
            return None, "Command 'drush " + ' '.join(cmd) + "' " \
                         "returned non-zero exit status 1"
        except OSError, e:
            return None, e.strerror
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

    def _extract_csv_from_output(self, output):
        """ Used to extract a CSV from the dirty remote drush output """
        regex = re.compile(r'\w+,[0-9x\-\.\w]*,[0-9x\-\.\w]*,[\w ]*\n')
        return re.findall(regex, output)


class NoJsonFoundError(Exception):
    pass


############################################################################

Plugin = CheckDrupalStatus

############################################################################


def main(argv=None):
    plugin = CheckDrupalStatus()
    plugin.execute(argv)


if __name__ == "__main__":
    main()