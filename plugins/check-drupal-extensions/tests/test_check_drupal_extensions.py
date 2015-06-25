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

from shinkenplugins.plugins.drupal_extensions import Plugin

LOCAL_DRUSH_OUTPUT = r"""{"percent":100,"label":"Extensions","checks":{"SiteAuditCheckExtensionsCount":{"label":"Count","description":"Count the number of enabled extensions (modules and themes) in a site.","result":"There are 36 extensions enabled.","action":null,"score":2},"SiteAuditCheckExtensionsDev":{"label":"Development","description":"Check for enabled development modules.","result":"No enabled development extensions were detected; no action required.","action":null,"score":2},"SiteAuditCheckExtensionsUnrecommended":{"label":"Not recommended","description":"Check for unrecommended modules.","result":"No unrecommended extensions were detected; no action required.","action":null,"score":2},"SiteAuditCheckExtensionsVersion":{"label":"Compatibility","description":"Check for specific versions of modules with known compatibility problems.","result":"No modules with specific version problems were detected; no action required.","action":null,"score":2},"SiteAuditCheckExtensionsDuplicate":{"label":"Duplicates","description":"Check for duplicate extensions in the site codebase.","result":"No duplicate extensions were detected.","action":null,"score":2},"SiteAuditCheckExtensionsMissing":{"label":"Missing","description":"Detect missing extensions (modules and themes) in a site, which degrades performance.","result":"No extensions are missing from your codebase.","action":null,"score":2},"SiteAuditCheckExtensionsDisabled":{"label":"Disabled modules","description":"Detect modules that have been disabled, but have not been uninstalled.","result":"No modules need to be uninstalled.","action":null,"score":2}}}"""
REMOTE_DRUSH_OUTPUT = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_WEDQmw --database=drupal --host=mysql --silent  < /tmp/drush_njdA6I
Only variables should be passed by reference Duplicate.php:91           [notice]
{"percent":100,"label":"Extensions","checks":{"SiteAuditCheckExtensionsCount":{"label":"Count","description":"Count the number of enabled extensions (modules and themes) in a site.","result":"There are 36 extensions enabled.","action":null,"score":2},"SiteAuditCheckExtensionsDev":{"label":"Development","description":"Check for enabled development modules.","result":"No enabled development extensions were detected; no action required.","action":null,"score":2},"SiteAuditCheckExtensionsUnrecommended":{"label":"Not recommended","description":"Check for unrecommended modules.","result":"No unrecommended extensions were detected; no action required.","action":null,"score":2},"SiteAuditCheckExtensionsVersion":{"label":"Compatibility","description":"Check for specific versions of modules with known compatibility problems.","result":"No modules with specific version problems were detected; no action required.","action":null,"score":2},"SiteAuditCheckExtensionsDuplicate":{"label":"Duplicates","description":"Check for duplicate extensions in the site codebase.","result":"No duplicate extensions were detected.","action":null,"score":2},"SiteAuditCheckExtensionsMissing":{"label":"Missing","description":"Detect missing extensions (modules and themes) in a site, which degrades performance.","result":"No extensions are missing from your codebase.","action":null,"score":2},"SiteAuditCheckExtensionsDisabled":{"label":"Disabled modules","description":"Detect modules that have been disabled, but have not been uninstalled.","result":"No modules need to be uninstalled.","action":null,"score":2}}}Command dispatch complete                                               [notice]
"""
EXPECTED_OUTPUT = r"""No enabled development extensions were detected;2;;No enabled development extensions were detected;2;;No duplicate extensions were detected.;2;;No extensions are missing from your codebase.;2;;No modules need to be uninstalled.;2;;"""


def _call_site_audit_mock(self, args):
    if self.home:
        return REMOTE_DRUSH_OUTPUT
    else:
        return LOCAL_DRUSH_OUTPUT


class Testdrupal_extensions(TestPlugin):
    def setUp(self):
        Plugin._call_site_audit = _call_site_audit_mock

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    def test_critical(self):
        args = ["-w", "140", "-c", "120", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT)

    def test_warning(self):
        args = ["-w", "110", "-c", "90", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT)

    def test_ok(self):
        args = ["-w", "70", "-c", "40", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_remote_critical(self):
        args = ["-w", "140", "-c", "120", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT)

    def test_remote_warning(self):
        args = ["-w", "110", "-c", "90", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT)

    def test_remote_ok(self):
        args = ["-w", "60", "-c", "30", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_incomplete_alias_arguments(self):
        expected = "--home-dir must be used with --alias"
        args = ["-w", "50", "-c", "70", "-a", "@drupal"]
        self.execute(Plugin, args, 3, stderr_pattern=expected)

    def test_incomplete_arguments(self):
        expected = "Either --alias and --home-dir or --drupal-path must be set"
        args = ["-w", "50", "-c", "70"]
        self.execute(Plugin, args, 3, stderr_pattern=expected)
        expected = "--warning and --critical are both required"
        args = []
        self.execute(Plugin, args, 3, stderr_pattern=expected)


if __name__ == '__main__':
    unittest.main()