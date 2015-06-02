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
#               2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import

import json
import requests
import subprocess
import lxml.html

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin

class CheckDrupalCore(ShinkenPlugin):
    NAME = 'drupal_core'
    VERSION = '1.0'
    DESCRIPTION = 'Check Drupal core version for known vulnerabilities'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'


    def __init__(self):
        super(CheckDrupalCore, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('-p', '--drupal-path', required=True,
                                 help='Drupal installation path'),

    def _get_drupal_core_version(self, path):
        try:
            data = self._call_drush(path)
            version = data.split('\n')[0].split(':')[1]
        except subprocess.CalledProcessError:
            return None, "Command 'drush status' " \
                         "returned non-zero exit status 1"
        except OSError, e:
            return None, e.strerror
        return version, None

    def _call_drush(self, path):
        out = subprocess.check_output(['drush', 'status'], cwd=path)
        return json.loads(out)

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckDrupalCore, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        return args

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        version = self._get_drupal_core_version(args.drupal_path)

        response = requests.get('http://www.cvedetails.com/version-search.php?'
                                'vendor=&product=drupal&version=%s' % version)

        root = lxml.html.fromstring(response.text)
        vulnerable = not root.xpath("//table/tr/td[@class='errormsg']")

        print vulnerable
        self.ok("Everything was perfect")



############################################################################

Plugin = CheckDrupalCore

############################################################################

def main(argv=None):
    plugin = CheckDrupalCore()
    plugin.execute(argv)


if __name__ == "__main__":
    main()