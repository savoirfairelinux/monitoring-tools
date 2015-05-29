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

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin
from shinkenplugins.states import STATES


class CheckDrupalCodebase(ShinkenPlugin):
    NAME = 'drupal_codebase'
    VERSION = '1.0'
    DESCRIPTION = 'A plugin to monitor Drupal codebase'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'

    def __init__(self):
        super(CheckDrupalCodebase, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('-p', '--drupal-path', required=True,
                                 help='Drupal installation path'),

    def _get_site_audit_result(self, path):
        try:
            data = self._call_site_audit(path)
        except subprocess.CalledProcessError:
            return None, "Command 'drush --json acb'" \
                         " returned non-zero exit status 1"
        except OSError, e:
            return None, e.strerror
        return data, None

    def _call_site_audit(self, path):
        out = subprocess.check_output(['drush', '--json', 'acb'], cwd=path)
        return json.loads(out)

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckDrupalCodebase, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        data, e_msg = self._get_site_audit_result(args.drupal_path)

        if data is None:
            self.unknown(e_msg)

        message = ['Codebase audit']
        message.append(
            '%s;' %
            data['checks']['SiteAuditCheckCodebaseSizeFiles']['result']
        )

        message.append(
            '%s;' %
            data['checks']['SiteAuditCheckCodebaseSizeAll']['result']
        )

        message.append(
            '%s' %
            data['checks']['SiteAuditCheckCodebaseManagedFileSize']['result']
        )

        self.ok('\n'.join(message))


############################################################################

Plugin = CheckDrupalCodebase

############################################################################


def main(argv=None):
    plugin = CheckDrupalCodebase()
    plugin.execute(argv)


if __name__ == "__main__":
    main()