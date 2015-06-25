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

from shinkenplugins.test import TestPlugin

from shinkenplugins.plugins.drupal_codebase import Plugin


LOCAL_DRUSH_OUTPUT = r"""{"percent":-1,"label":"Codebase","checks":{"SiteAuditCheckCodebaseSizeFiles":{"label":"Size of sites\/default\/files","description":"Determine the size of sites\/default\/files.","result":"Files: 24kB","action":null,"score":-1},"SiteAuditCheckCodebaseSizeAll":{"label":"Size of entire site","description":"Determine the size of the site root; does not include remote mounts.","result":"Total size: 14.96MB","action":null,"score":-1},"SiteAuditCheckCodebaseManagedFileCount":{"label":"Drupal managed file count","description":"Determine the count of Drupal managed files.","result":"Managed file count: 0","action":null,"score":-1},"SiteAuditCheckCodebaseManagedFileSize":{"label":"Drupal managed file size","description":"Determine the size of Drupal managed files.","result":"Managed file size: 0.00kB","action":null,"score":-1}}}"""
REMOTE_DRUSH_OUTPUT = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_qVA8xD --database=drupal --host=mysql --silent  < /tmp/drush_Lyzz1T
{"percent":-1,"label":"Codebase","checks":{"SiteAuditCheckCodebaseSizeFiles":{"label":"Size of sites\/default\/files","description":"Determine the size of sites\/default\/files.","result":"Files: 24kB","action":null,"score":-1},"SiteAuditCheckCodebaseSizeAll":{"label":"Size of entire site","description":"Determine the size of the site root; does not include remote mounts.","result":"Total size: 14.96MB","action":null,"score":-1},"SiteAuditCheckCodebaseManagedFileCount":{"label":"Drupal managed file count","description":"Determine the count of Drupal managed files.","result":"Managed file count: 0","action":null,"score":-1},"SiteAuditCheckCodebaseManagedFileSize":{"label":"Drupal managed file size","description":"Determine the size of Drupal managed files.","result":"Managed file size: 0.00kB","action":null,"score":-1}}}Command dispatch complete                                               [notice]
"""
EXPECTED_OUTPUT = r"""Files: 24kB;-1;;Total size: 14.96MB;-1;;Managed file size: 0.00kB;-1;;"""


def _call_site_audit_mock(self, args):
    if self.home:
        return REMOTE_DRUSH_OUTPUT
    else:
        return LOCAL_DRUSH_OUTPUT


class Testdrupal_codebase(TestPlugin):
    def setUp(self):
        Plugin._call_site_audit = _call_site_audit_mock

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    def test_local(self):
        args = ["-p", "/var/www/html/"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_remote(self):
        args = ["-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_incomplete_alias_arguments(self):
        expected = "--home-dir must be used with --alias"
        args = ["-a", "@drupal"]
        self.execute(Plugin, args, 3, stderr_pattern=expected)

    def test_incomplete_arguments(self):
        expected = "Either --alias and --home-dir or --drupal-path must be set"
        args = []
        self.execute(Plugin, args, 3, stderr_pattern=expected)


if __name__ == '__main__':
    unittest.main()