#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Keystone monitoring script for Nagios
#
# Copyright (C) 2014 Savoir-faire Linux Inc.
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Alexandre Viau <alexandre.viau@savoirfairelinux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import requests
import datetime

from shinkenplugins.old import BasePlugin
from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES

from keystoneclient.v2_0 import client as ksclient


class Plugin(BasePlugin):
    NAME = 'check-nova'
    VERSION = '0.1'
    DESCRIPTION = 'check nova'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre.viau@savoirfairelinux.com'

    ARGS = [
        # Can't touch this:
        ('h', 'help', 'display plugin help', False),
        ('v', 'version', 'display plugin version number', False),
        # Add your plugin arguments here:
        # ('short', 'long', 'description', 'does it expect a value?')

        # OpenStack Auth
        ('U', 'auth_url', 'Keystone auth URL', True),
        ('e', 'nova_endpoint', 'Nova v2.1 endpoint', True),
        ('u', 'username', 'username to use for authentication', True),
        ('p', 'password', 'password to use for authentication', True),
        ('t', 'tenant', 'tenant name to use for authentication', True),

        # Options
        ('f', 'flavors', "comma-separated flavors to check for", True),
    ]

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        if not args.get('help') and not args.get('version'):
            for arg in [
                'auth_url',
                'username',
                'password',
                'tenant',
                'nova_endpoint',
            ]:
                if arg not in args.keys():
                    return False, 'the argument %s must be present' % arg

            if 'flavors' in args.keys():
                args['flavors'] = args['flavors'].split(',')
            else:
                args['flavors'] = []

        return True, None

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        perfdata = []
        expected_flavors = args['flavors']

        try:
            c = ksclient.Client(
                username=args['username'],
                tenant_name=args['tenant'],
                password=args['password'],
                auth_url=args['auth_url'],
            )

            token = c.auth_token
            tenant_id = c.auth_ref['token']['tenant']['id']

        except Exception as e:
            self.exit(STATES.UNKNOWN, "Authentification failed: " + str(e))

        try:
            headers = {
                "X-Auth-Token": token,
                "content-type": "application/json",
                "accept": "application/json",
            }

            start_time = datetime.datetime.now()
            resp = requests.get(
                "%s/%s/flavors" % (args['nova_endpoint'], tenant_id),
                headers=headers
            )
            end_time = datetime.datetime.now()

            perfdata.append(
                PerfData(
                    'flavor_list_time',
                    ((end_time - start_time).total_seconds()/1000),
                    min_='0',
                    unit='ms'
                )
            )

            flavors = resp.json()
            flavors_names = [f['name'] for f in flavors['flavors']]
            perfdata.append(PerfData('flavors_count', len(flavors_names), min_='0'))
        except Exception as e:
            self.exit(STATES.UNKNOWN, "Could not list flavors" + str(e))

        msgs = []
        for flavor in expected_flavors:
            if flavor not in flavors_names:
                msgs.append("'%s' flavor is missing" % flavor)

        if len(msgs) > 0:
            self.exit(
                STATES.CRITICAL,
                ' '.join(msgs),
                *perfdata
            )
        else:
            self.exit(
                STATES.OK,
                "Nova API OK",
                *perfdata
            )


def main(argv=None):
    Plugin(argv)

if __name__ == "__main__":
    main()
