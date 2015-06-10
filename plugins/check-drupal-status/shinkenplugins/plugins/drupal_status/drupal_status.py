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


class CheckDrupalStatus(ShinkenPlugin):
    NAME = 'drupal_status'
    VERSION = '1.0'
    DESCRIPTION = 'A plugin to monitor Drupal status'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'

    def __init__(self):
        super(CheckDrupalStatus, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('-p', '--drupal-path', required=True,
                                 help='Drupal installation path'),

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckDrupalStatus, self).parse_args(args)
        return args

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        self.path = args.drupal_path

        data, e_msg = self._get_site_audit_result()
        update_status, e_msg = self._get_update_status()

        if data is None or e_msg is not None:
            self.unknown(e_msg)

        info = data['checks']['SiteAuditCheckStatusSystem']['result']
        info = info.split('\n')
        info = {line.split(':')[0]: line.split(':')[1] for line in info}

        update_status = update_status.strip().split('\n')

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

    def _get_site_audit_result(self):
        try:
            data = self._call_site_audit(['--json', '--detail', 'as'])
            data = json.loads(data)
        except subprocess.CalledProcessError, e:
            return None, "Command 'drush --json --detail as' " \
                         "returned non-zero exit status 1"
        except OSError, e:
            return None, e.strerror
        return data, None

    def _get_update_status(self):
        try:
            data = self._call_site_audit(['ups', '--format=csv'])
        except subprocess.CalledProcessError, e:
            return None, "Command 'drush ups --format=csv' " \
                         "returned non-zero exit status 1"
        except OSError, e:
            return None, e.strerror
        return data, None

    def _call_site_audit(self, args):
        cmd = ['drush']
        [cmd.append(arg) for arg in args]

        with open('/dev/null', 'w') as devnull:
            out = subprocess.check_output(cmd, cwd=self.path, stderr=devnull)

        return out


############################################################################

Plugin = CheckDrupalStatus

############################################################################


def main(argv=None):
    plugin = CheckDrupalStatus()
    plugin.execute(argv)


if __name__ == "__main__":
    main()