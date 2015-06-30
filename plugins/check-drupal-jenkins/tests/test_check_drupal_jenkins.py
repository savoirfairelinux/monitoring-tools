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

# Copyright (C) 2014, Frédéric Vachon <frederic.vachon@savoirfairelinux.com>

import unittest

import requests
import requests_mock

from shinkenplugins.test import TestPlugin
from shinkenplugins.plugins.drupal_jenkins import Plugin


SESSION_URL_CALL_COUNTER = 0


def session_matcher(request):
    global SESSION_URL_CALL_COUNTER

    username = "j_username=user"
    password = "j_password=password"

    response = None

    if request._request.url == r"https://jenkins.nodejs.org/j_acegi_security_check" and \
       request._request.method == "POST":
        response = requests.Response()
        if SESSION_URL_CALL_COUNTER == 0:
            response.status_code = 200
        else:
            response.status_code = 301
            if username in request.text and \
               password in request.text:
                response.status_code = 200


    SESSION_URL_CALL_COUNTER += 1
    return response


class Testdrupal_jenkins(TestPlugin):
    def setUp(self):
        global SESSION_URL_CALL_COUNTER
        SESSION_URL_CALL_COUNTER = 0

        self.JSON_RESPONSE_SUCCESS = r"""{
            "building": false,
            "description": null,
            "duration": 190920,
            "estimatedDuration": 203722,
            "executor": null,
            "fullDisplayName": "node-build-ubuntu-12.04 #3124",
            "id": "2014-02-06_15-59-21",
            "keepLog": false,
            "number": 3124,
            "result": "SUCCESS",
            "timestamp": 1391702361000,
            "url": "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/3124/",
            "builtOn": "windows-2k8r2"
        }"""

        self.JSON_RESPONSE_UNSTABLE = r"""{
            "building": false,
            "description": null,
            "duration": 190920,
            "estimatedDuration": 203722,
            "executor": null,
            "fullDisplayName": "node-build-ubuntu-12.04 #3124",
            "id": "2014-02-06_15-59-21",
            "keepLog": false,
            "number": 3124,
            "result": "UNSTABLE",
            "timestamp": 1391702361000,
            "url": "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/3124/",
            "builtOn": "windows-2k8r2"
        }"""

        self.JSON_RESPONSE_FAILURE = r"""{
            "building": false,
            "description": null,
            "duration": 190920,
            "estimatedDuration": 203722,
            "executor": null,
            "fullDisplayName": "node-build-ubuntu-12.04 #3124",
            "id": "2014-02-06_15-59-21",
            "keepLog": false,
            "number": 3124,
            "result": "FAILURE",
            "timestamp": 1391702361000,
            "url": "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/3124/",
            "builtOn": "windows-2k8r2"
        }"""

        self.JSON_RESPONSE_UNKNOWN = r"""{
            "building": false,
            "description": null,
            "duration": 190920,
            "estimatedDuration": 203722,
            "executor": null,
            "fullDisplayName": "node-build-ubuntu-12.04 #3124",
            "id": "2014-02-06_15-59-21",
            "keepLog": false,
            "number": 3124,
            "result": "DISABLED",
            "timestamp": 1391702361000,
            "url": "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/3124/",
            "builtOn": "windows-2k8r2"
        }"""

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    @requests_mock.mock()
    def test_build_success(self, m):
        m.get("http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/"
              "lastCompletedBuild/api/json",
              text=self.JSON_RESPONSE_SUCCESS)

        expected = 'Last build was successful'
        args = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04"]
        self.execute(Plugin, args, 0, expected)

    @requests_mock.mock()
    def test_build_unstable(self, m):
        m.get("http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/"
              "lastCompletedBuild/api/json",
              text=self.JSON_RESPONSE_UNSTABLE)

        expected = 'Last build was unstable'
        args = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04"]
        self.execute(Plugin, args, 1, expected)

    @requests_mock.mock()
    def test_build_failure(self, m):
        m.get("http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/"
              "lastCompletedBuild/api/json",
              text=self.JSON_RESPONSE_FAILURE)

        expected = 'Last build failed'
        args = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04"]
        self.execute(Plugin, args, 2, expected)

    @requests_mock.mock()
    def test_build_unknown(self, m):
        m.get("http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/"
              "lastCompletedBuild/api/json",
              text=self.JSON_RESPONSE_UNKNOWN)

        expected = 'Last build ended in a unknown state'
        args = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04"]
        self.execute(Plugin, args, 3, expected)

    @requests_mock.mock()
    def test_bad_jenkins_response(self, m):
        m.get("http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/"
              "lastCompletedBuild/api/json",
              text=self.JSON_RESPONSE_UNKNOWN,
              status_code=500)

        expected = 'Unexpected Jenkins response'
        args = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04"]
        self.execute(Plugin, args, 3, expected)

    @requests_mock.mock()
    def test_authentication(self, m):
        m.add_matcher(session_matcher)

        m.get("http://jenkins.nodejs.org/job/node-build-ubuntu-12.04/"
              "lastCompletedBuild/api/json",
              text=self.JSON_RESPONSE_SUCCESS)

        expected = 'Last build was successful'
        args = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04",
                "-a", "https://jenkins.nodejs.org/j_acegi_security_check",
                "-n", "user", "-p", "password"]

        self.execute(Plugin, args, 0, expected)

    def test_missing_url_arg(self):
        args = []
        expected = 'error: argument -u/--url is required'

        self.execute(Plugin, args, 3, stderr_pattern=expected)

    def test_auth_missing_args(self):
        args1 = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04",
                 "-a", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04",
                 "-n", "user"]
        args2 = ["-u", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04",
                 "-a", "http://jenkins.nodejs.org/job/node-build-ubuntu-12.04",
                 "-p", "password"]

        expected = '--auth-username and --auth-password are ' \
                   'both required when using --auth-url'

        self.execute(Plugin, args1, 3, stderr_pattern=expected)
        self.execute(Plugin, args2, 3, stderr_pattern=expected)


if __name__ == '__main__':
    unittest.main()