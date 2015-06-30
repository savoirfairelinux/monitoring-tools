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

from shinkenplugins.plugins.drupal_cache import Plugin

LOCAL_DRUSH_OUTPUT = r"""{"percent":17,"label":"Drupal's caching settings","checks":{"SiteAuditCheckCacheAnon":{"label":"Anonymous caching","description":"Verify Drupal's anonymous page caching is enabled.","result":"Anonymous page caching is not enabled!","action":"Go to \/admin\/config\/development\/performance and check \"Cache pages for anonymous users\".","score":0},"SiteAuditCheckCacheLifetime":{"label":"Minimum cache lifetime","description":"Verify that Drupal's minimum cache lifetime is set to never expire.","result":"Minimum cache lifetime is set to none.","action":null,"score":2},"SiteAuditCheckCachePageExpire":{"label":"Expiration of cached pages","description":"Verify that Drupal's cached pages last for at least 15 minutes.","result":"Expiration of cached pages not set!","action":"Go to \/admin\/config\/development\/performance and set \"Expiration of cached pages\" to 15 min or above.","score":0},"SiteAuditCheckCachePageCompression":{"label":"Cached page compression","description":"Verify that Drupal is set to compress cached pages.","result":"Cached pages are not compressed!","action":"Go to \/admin\/config\/development\/performance and check \"Compress cached pages\".","score":0},"SiteAuditCheckCachePreprocessCss":{"label":"Aggregate and compress CSS files in Drupal","description":"Verify that Drupal is aggregating and compressing CSS.","result":"CSS aggregation and compression is not enabled!","action":"Go to \/admin\/config\/development\/performance and check \"Aggregate and compress CSS files\".","score":0},"SiteAuditCheckCachePreprocessJs":{"label":"Aggregate JavaScript files in Drupal","description":"Verify that Drupal is aggregating JavaScript.","result":"JavaScript aggregation is not enabled!","action":"Go to \/admin\/config\/development\/performance and check \"Aggregate JavaScript files\".","score":0},"SiteAuditCheckCacheLock":{"label":"Lock API","description":"Determine the default locking mechanism.","result":"Using the default semaphore database table.","action":"Consider using a dedicated API to a caching backend, such as redis or memcache.","score":-1},"SiteAuditCheckCacheBackends":{"label":"Caching backends","description":"Detail caching backends.","result":"Using the database as a caching backend, which is less efficient than a dedicated key-value store.","action":"Consider using a caching backend such as redis or memcache.","score":-1},"SiteAuditCheckCacheDefaultClass":{"label":"Default class","description":"Determine the default cache class, used whenever no alternative is specified.","result":"Using DrupalDatabaseCache.","action":null,"score":-1},"SiteAuditCheckCacheBins":{"label":"Cache bins","description":"Detail explicitly defined cache bins.","result":"Bin: Class\n----------\ncache_class_cache_ctools_css: CToolsCssCache","action":null,"score":-1}}}"""
REMOTE_DRUSH_OUTPUT = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_H7zdwR --database=drupal --host=mysql --silent  < /tmp/drush_j19QEE
Undefined index: cache Anon.php:62                                      [notice]
Undefined index: page_compression PageCompression.php:86                [notice]
Undefined index: preprocess_css PreprocessCss.php:62                    [notice]
Undefined index: preprocess_js PreprocessJs.php:62                      [notice]
{"percent":17,"label":"Drupal's caching settings","checks":{"SiteAuditCheckCacheAnon":{"label":"Anonymous caching","description":"Verify Drupal's anonymous page caching is enabled.","result":"Anonymous page caching is not enabled!","action":"Go to \/admin\/config\/development\/performance and check \"Cache pages for anonymous users\".","score":0},"SiteAuditCheckCacheLifetime":{"label":"Minimum cache lifetime","description":"Verify that Drupal's minimum cache lifetime is set to never expire.","result":"Minimum cache lifetime is set to none.","action":null,"score":2},"SiteAuditCheckCachePageExpire":{"label":"Expiration of cached pages","description":"Verify that Drupal's cached pages last for at least 15 minutes.","result":"Expiration of cached pages not set!","action":"Go to \/admin\/config\/development\/performance and set \"Expiration of cached pages\" to 15 min or above.","score":0},"SiteAuditCheckCachePageCompression":{"label":"Cached page compression","description":"Verify that Drupal is set to compress cached pages.","result":"Cached pages are not compressed!","action":"Go to \/admin\/config\/development\/performance and check \"Compress cached pages\".","score":0},"SiteAuditCheckCachePreprocessCss":{"label":"Aggregate and compress CSS files in Drupal","description":"Verify that Drupal is aggregating and compressing CSS.","result":"CSS aggregation and compression is not enabled!","action":"Go to \/admin\/config\/development\/performance and check \"Aggregate and compress CSS files\".","score":0},"SiteAuditCheckCachePreprocessJs":{"label":"Aggregate JavaScript files in Drupal","description":"Verify that Drupal is aggregating JavaScript.","result":"JavaScript aggregation is not enabled!","action":"Go to \/admin\/config\/development\/performance and check \"Aggregate JavaScript files\".","score":0},"SiteAuditCheckCacheLock":{"label":"Lock API","description":"Determine the default locking mechanism.","result":"Using the default semaphore database table.","action":"Consider using a dedicated API to a caching backend, such as redis or memcache.","score":-1},"SiteAuditCheckCacheBackends":{"label":"Caching backends","description":"Detail caching backends.","result":"Using the database as a caching backend, which is less efficient than a dedicated key-value store.","action":"Consider using a caching backend such as redis or memcache.","score":-1},"SiteAuditCheckCacheDefaultClass":{"label":"Default class","description":"Determine the default cache class, used whenever no alternative is specified.","result":"Using DrupalDatabaseCache.","action":null,"score":-1},"SiteAuditCheckCacheBins":{"label":"Cache bins","description":"Detail explicitly defined cache bins.","result":"Bin: Class\n----------\ncache_class_cache_ctools_css: CToolsCssCache","action":null,"score":-1}}}Command dispatch complete                                               [notice]
"""
EXPECTED_OUTPUT = r"""Anonymous page caching is not enabled!;0;Go to /admin/config/development/performance and check "Cache pages for anonymous users".;Minimum cache lifetime is set to none.;2;;Expiration of cached pages not set!;0;Go to /admin/config/development/performance and set "Expiration of cached pages" to 15 min or above.;Cached pages are not compressed!;0;Go to /admin/config/development/performance and check "Compress cached pages".;CSS aggregation and compression is not enabled!;0;Go to /admin/config/development/performance and check "Aggregate and compress CSS files".;JavaScript aggregation is not enabled!;0;Go to /admin/config/development/performance and check "Aggregate JavaScript files".;Using the default semaphore database table.;-1;Consider using a dedicated API to a caching backend, such as redis or memcache.;Using the database as a caching backend, which is less efficient than a dedicated key-value store.;-1;Consider using a caching backend such as redis or memcache.;Bin: Class
----------
cache_class_cache_ctools_css: CToolsCssCache;-1;;"""


def _call_site_audit_mock(self, args):
    if self.home:
        return REMOTE_DRUSH_OUTPUT
    else:
        return LOCAL_DRUSH_OUTPUT


class Testdrupal_cache(TestPlugin):
    def setUp(self):
        Plugin._call_site_audit = _call_site_audit_mock

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    def test_critical(self):
        args = ["-w", "70", "-c", "50", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT)

    def test_warning(self):
        args = ["-w", "20", "-c", "5", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT)

    def test_ok(self):
        args = ["-w", "15", "-c", "5", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT)

    def test_remote_critical(self):
        args = ["-w", "70", "-c", "50", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT)

    def test_remote_warning(self):
        args = ["-w", "20", "-c", "10", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT)

    def test_remote_ok(self):
        args = ["-w", "10", "-c", "5", "-a", "@drupal", "-d", "/home/alignak"]
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