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

from shinkenplugins.plugins.drupal_views import Plugin

LOCAL_DRUSH_OUTPUT = r"""{"percent":50,"label":"Views","checks":{"SiteAuditCheckViewsEnabled":{"label":"Views status","description":"Check to see if enabled","result":"Views is enabled.","action":null,"score":2},"SiteAuditCheckViewsCount":{"label":"Count","description":"Number of enabled Views.","result":"There are 4 enabled views.","action":null,"score":2},"SiteAuditCheckViewsCacheResults":{"label":"Query results caching","description":"Check the length of time raw query results should be cached.","result":"No View is caching query results!","action":"Query results should be cached for at least 1 minute.","score":0},"SiteAuditCheckViewsCacheOutput":{"label":"Rendered output caching","description":"Check the length of time raw rendered output should be cached.","result":"No View is caching rendered output!","action":"Rendered output should be cached for as long as possible (if the query changes, the output will be refreshed).","score":0}}}"""
LOCAL_DRUSH_OUTPUT_DISABLE = r"""{"percent":-1,"label":"Views","checks":{"SiteAuditCheckViewsEnabled":{"label":"Views status","description":"Check to see if enabled","result":"Views is not enabled.","action":null,"score":-1}}}"""
REMOTE_DRUSH_OUTPUT = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_fOiPyL --database=drupal --host=mysql --silent  < /tmp/drush_BGJTIn
{"percent":50,"label":"Views","checks":{"SiteAuditCheckViewsEnabled":{"label":"Views status","description":"Check to see if enabled","result":"Views is enabled.","action":null,"score":2},"SiteAuditCheckViewsCount":{"label":"Count","description":"Number of enabled Views.","result":"There are 4 enabled views.","action":null,"score":2},"SiteAuditCheckViewsCacheResults":{"label":"Query results caching","description":"Check the length of time raw query results should be cached.","result":"No View is caching query results!","action":"Query results should be cached for at least 1 minute.","score":0},"SiteAuditCheckViewsCacheOutput":{"label":"Rendered output caching","description":"Check the length of time raw rendered output should be cached.","result":"No View is caching rendered output!","action":"Rendered output should be cached for as long as possible (if the query changes, the output will be refreshed).","score":0}}}Command dispatch complete                                               [notice]
"""
REMOTE_DRUSH_OUTPUT_DISABLE = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_V62EaV --database=drupal --host=mysql --silent  < /tmp/drush_t7tsqX
{"percent":-1,"label":"Views","checks":{"SiteAuditCheckViewsEnabled":{"label":"Views status","description":"Check to see if enabled","result":"Views is not enabled.","action":null,"score":-1}}}Command dispatch complete                                               [notice]
"""
EXPECTED_OUTPUT = r"""Views is enabled.;2;;There are 4 enabled views.;2;;No View is caching query results!;0;Query results should be cached for at least 1 minute.;No View is caching rendered output!;0;Rendered output should be cached for as long as possible \(if the query changes, the output will be refreshed\).;"""
EXPECTED_OUTPUT_DISABLED = r"""Views is not enabled."""

FORCE_DISABLE_VIEWS = False


def _call_site_audit_mock(self, args):
    global FORCE_DISABLE_VIEWS
    if self.home:
        if FORCE_DISABLE_VIEWS:
            return REMOTE_DRUSH_OUTPUT_DISABLE
        return REMOTE_DRUSH_OUTPUT
    else:
        if FORCE_DISABLE_VIEWS:
            return LOCAL_DRUSH_OUTPUT_DISABLE
        return LOCAL_DRUSH_OUTPUT


class Testdrupal_views(TestPlugin):
    def setUp(self):
        global FORCE_DISABLE_VIEWS
        FORCE_DISABLE_VIEWS = False
        Plugin._call_site_audit = _call_site_audit_mock

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    def test_critical(self):
        args = ["-w", "80", "-c", "60", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT)

    def test_warning(self):
        args = ["-w", "60", "-c", "40", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT)

    def test_ok(self):
        args = ["-w", "40", "-c", "20", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_remote_critical(self):
        args = ["-w", "80", "-c", "60", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT)

    def test_remote_warning(self):
        args = ["-w", "60", "-c", "40", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT)

    def test_remote_ok(self):
        args = ["-w", "40", "-c", "20", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_remote_views_disabled(self):
        global FORCE_DISABLE_VIEWS
        FORCE_DISABLE_VIEWS = True
        args = ["-w", "40", "-c", "20", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT_DISABLED)

    def test_views_disabled(self):
        global FORCE_DISABLE_VIEWS
        FORCE_DISABLE_VIEWS = True
        args = ["-w", "40", "-c", "20", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT_DISABLED)

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