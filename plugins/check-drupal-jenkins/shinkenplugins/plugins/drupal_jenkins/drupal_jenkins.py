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

from shinkenplugins.plugin import ShinkenPlugin


class CheckDrupalJenkins(ShinkenPlugin):
    NAME = 'drupal_jenkins'
    VERSION = '1.0'
    DESCRIPTION = 'A plugin to monitor Drupal last build using Jenkins API'
    AUTHOR = 'Frédéric Vachon'
    EMAIL = 'frederic.vachon@savoirfairelinux.com'

    def __init__(self):
        super(CheckDrupalJenkins, self).__init__()
        self.parser.add_argument('-u', '--url', required=True,
                                 help='The Jenkins job URL')
        self.parser.add_argument('-a', '--auth-url', required=False,
                                 help='The Jenkins authentication URL')
        self.parser.add_argument('-n', '--auth-username', required=False,
                                 help='Username for authentication')
        self.parser.add_argument('-p', '--auth-password', required=False,
                                 help='Username for authentication')

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckDrupalJenkins, self).parse_args(args)
        if args.auth_url:
            if None in (args.auth_username, args.auth_password):
                self.parser.error('--auth-username and --auth-password are '
                                  'both required when using --auth-url')
        return args

    def run(self, args):
        """ Main Plugin function """
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        self.auth_url = args.auth_url
        self.url = args.url

        try:
            self._create_session(args.auth_username, args.auth_password)
            result = self._last_build_result()
        except Exception, e:
            self.unknown(e.message)

        if result == 'SUCCESS':
            self.ok('Last build was successful')
        elif result == 'UNSTABLE':
            self.warning('Last build was unstable')
        elif result == 'FAILURE':
            self.critical('Last build failed')
        else:
            self.unknown('Last build ended in a unknown state')

    def _create_session(self, username, password):
        self.session = requests.session()

        if username and password:
            self._authenticate(username, password)

    def _authenticate(self, username, password):
        creds = {
            "j_username": username,
            "j_password": password,
            "remember_me": True,
            "from": "/"
        }

        # Need to send the request twice because the user need to get
        # a session cookie before he can authenticate
        self.session.post(self.auth_url)
        resp = self.session.post(self.auth_url, data=creds)

        if resp.status_code is not 200:
            raise Exception('Authentication Failed')

    def _last_build_result(self):
        resp = self.session.get(self.url + '/lastCompletedBuild/api/json',
                                verify=False)

        if resp.status_code is not 200:
            raise Exception('Unexpected Jenkins response')

        data = json.loads(resp.text)

        return data['result']


############################################################################

Plugin = CheckDrupalJenkins

############################################################################


def main(argv=None):
    plugin = CheckDrupalJenkins()
    plugin.execute(argv)


if __name__ == "__main__":
    main()