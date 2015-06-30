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

from shinkenplugins.plugins.drupal_status import Plugin

LOCAL_DRUSH_CMD1_OUTPUT = r"""{"percent":70,"label":"Status","checks":{"SiteAuditCheckStatusSystem":{"label":"System Status","description":"Drupal's status report.","result":"Drupal: Info - 7.37\nAccess to update.php: Info - Protected\nCTools CSS Cache: Error - Unable to create\nConfiguration file: Info - Protected\nCron maintenance tasks: Ok - Last run 43 min 31 sec ago\nDatabase system: Info - MySQL, MariaDB, or equivalent\nDatabase system version: Info - 5.6.25\nDatabase updates: Ok - Up to date\nDrupal core update status: Error - Not secure! (version 7.38 available)\nFile system: Info - Writable (public download method)\nGD library PNG support: Ok - bundled (2.1.0 compatible)\nGD library rotate and desaturate effects: Ok - bundled (2.1.0 compatible)\nModule and theme update status: Error - Not secure!\nNode Access Permissions: Info - Disabled\nPHP: Info - 5.6.9 (more information)\nPHP extensions: Info - Enabled\nPHP memory limit: Info - 128M\nPHP register globals: Info - Disabled\nUnicode library: Ok - PHP Mbstring Extension\nUpdate notifications: Info - Enabled\nUpload progress: Info - Not enabled\nWeb server: Info","action":null,"score":1}}}"""
LOCAL_DRUSH_CMD2_OUTPUT = r"""drupal,7.37,7.38,SECURITY UPDATE available
advanced_forum,7.x-2.1,7.x-2.5,Update available
ctools,7.x-1.7,7.x-1.7,Up to date
panels,7.x-3.1,7.x-3.5,Update available
views,7.x-3.1,7.x-3.11,SECURITY UPDATE available
"""
LOCAL_DRUSH_CMD2_OUTPUT_WARN = r""" advanced_forum,7.x-2.1,7.x-2.5,Update available
ctools,7.x-1.7,7.x-1.7,Up to date
panels,7.x-3.1,7.x-3.5,Update available
"""
LOCAL_DRUSH_CMD2_OUTPUT_OK = r"""ctools,7.x-1.7,7.x-1.7,Up to date"""
LOCAL_DRUSH_CMD3_OUTPUT = r"""Chaos tool suite,Bulk Export (bulk_export),Module,Not installed,7.x-1.7
Chaos tool suite,Chaos tools (ctools),Module,Enabled,7.x-1.7
Chaos tool suite,Chaos Tools (CTools) AJAX Example (ctools_ajax_sample),Module,Not installed,7.x-1.7
Chaos tool suite,Chaos Tools (CTools) Plugin Example (ctools_plugin_example),Module,Not installed,7.x-1.7
Chaos tool suite,Custom content panes (ctools_custom_content),Module,Not installed,7.x-1.7
Chaos tool suite,Custom rulesets (ctools_access_ruleset),Module,Not installed,7.x-1.7
Chaos tool suite,Page manager (page_manager),Module,Not installed,7.x-1.7
Chaos tool suite,Stylizer (stylizer),Module,Not installed,7.x-1.7
Chaos tool suite,Term Depth access (term_depth),Module,Not installed,7.x-1.7
Chaos tool suite,Views content panes (views_content),Module,Not installed,7.x-1.7
Core,Aggregator (aggregator),Module,Not installed,7.37
Core,Block (block),Module,Enabled,7.37
Core,Blog (blog),Module,Not installed,7.37
Core,Book (book),Module,Not installed,7.37
Core,Color (color),Module,Enabled,7.37
Core,Comment (comment),Module,Enabled,7.37
Core,Contact (contact),Module,Not installed,7.37
Core,Content translation (translation),Module,Not installed,7.37
Core,Contextual links (contextual),Module,Enabled,7.37
Core,Dashboard (dashboard),Module,Enabled,7.37
Core,Database logging (dblog),Module,Enabled,7.37
Core,Field (field),Module,Enabled,7.37
Core,Field SQL storage (field_sql_storage),Module,Enabled,7.37
Core,Field UI (field_ui),Module,Enabled,7.37
Core,File (file),Module,Enabled,7.37
Core,Filter (filter),Module,Enabled,7.37
Core,Forum (forum),Module,Enabled,7.37
Core,Help (help),Module,Enabled,7.37
Core,Image (image),Module,Enabled,7.37
Core,List (list),Module,Enabled,7.37
Core,Locale (locale),Module,Not installed,7.37
Core,Menu (menu),Module,Enabled,7.37
Core,Node (node),Module,Enabled,7.37
Core,Number (number),Module,Enabled,7.37
Core,OpenID (openid),Module,Not installed,7.37
Core,Options (options),Module,Enabled,7.37
Core,Overlay (overlay),Module,Enabled,7.37
Core,Path (path),Module,Enabled,7.37
Core,PHP filter (php),Module,Not installed,7.37
Core,Poll (poll),Module,Not installed,7.37
Core,RDF (rdf),Module,Enabled,7.37
Core,Search (search),Module,Enabled,7.37
Core,Shortcut (shortcut),Module,Enabled,7.37
Core,Statistics (statistics),Module,Not installed,7.37
Core,Syslog (syslog),Module,Not installed,7.37
Core,System (system),Module,Enabled,7.37
Core,Taxonomy (taxonomy),Module,Enabled,7.37
Core,Testing (simpletest),Module,Not installed,7.37
Core,Text (text),Module,Enabled,7.37
Core,Toolbar (toolbar),Module,Enabled,7.37
Core,Tracker (tracker),Module,Not installed,7.37
Core,Trigger (trigger),Module,Not installed,7.37
Core,Update manager (update),Module,Enabled,7.37
Core,User (user),Module,Enabled,7.37
Other,Advanced Forum (advanced_forum),Module,Enabled,7.x-2.1
Panels,Mini panels (panels_mini),Module,Not installed,7.x-3.1
Panels,Panel nodes (panels_node),Module,Not installed,7.x-3.1
Panels,Panels (panels),Module,Enabled,7.x-3.1
Panels,Panels In-Place Editor (panels_ipe),Module,Not installed,7.x-3.1
Views,Views (views),Module,Enabled,7.x-3.1
Views,Views UI (views_ui),Module,Not installed,7.x-3.1
Core,Bartik (bartik),Theme,Enabled,7.37
Core,Garland (garland),Theme,Disabled,7.37
Core,Seven (seven),Theme,Enabled,7.37
Core,Stark (stark),Theme,Disabled,7.37
"""
REMOTE_DRUSH_CMD1_OUTPUT = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_mu5Bxx --database=drupal --host=mysql --silent  < /tmp/drush_89MwGo
{"percent":73,"label":"Status","checks":{"SiteAuditCheckStatusSystem":{"label":"System Status","description":"Drupal's status report.","result":"Drupal: Info - 7.37\nAccess to update.php: Info - Protected\nCTools CSS Cache: Ok - Exists\nConfiguration file: Info - Protected\nCron maintenance tasks: Ok - Last run 46 min 44 sec ago\nDatabase system: Info - MySQL, MariaDB, or equivalent\nDatabase system version: Info - 5.6.25\nDatabase updates: Ok - Up to date\nDrupal core update status: Error - Not secure! (version 7.38 available)\nFile system: Error - Writable (public download method)\nGD library PNG support: Ok - bundled (2.1.0 compatible)\nGD library rotate and desaturate effects: Ok - bundled (2.1.0 compatible)\nModule and theme update status: Error - Not secure!\nNode Access Permissions: Info - Disabled\nPHP: Info - 5.6.9 (more information)\nPHP extensions: Info - Enabled\nPHP memory limit: Info - 128M\nPHP register globals: Info - Disabled\nUnicode library: Ok - PHP Mbstring Extension\nUpdate notifications: Info - Enabled\nUpload progress: Info - Not enabled\nWeb server: Info","action":null,"score":1}}}Command dispatch complete                                               [notice]
"""
REMOTE_DRUSH_CMD2_OUTPUT = r"""/home/nagios/.drush/cache/download/https---updates.drupal.org-release-history-views-7.x   [notice]
retrieved from cache.
drupal,7.37,7.38,SECURITY UPDATE available
advanced_forum,7.x-2.1,7.x-2.5,Update available
ctools,7.x-1.7,7.x-1.7,Up to date
panels,7.x-3.1,7.x-3.5,Update available
views,7.x-3.1,7.x-3.11,SECURITY UPDATE available
Command dispatch complete                                               [notice]
"""
REMOTE_DRUSH_CMD2_OUTPUT_OK = r"""/home/nagios/.drush/cache/download/https---updates.drupal.org-release-history-views-7.x   [notice]
retrieved from cache.
ctools,7.x-1.7,7.x-1.7,Up to date
Command dispatch complete                                               [notice]
"""
REMOTE_DRUSH_CMD2_OUTPUT_WARN = r"""Downloading release history from                                        [notice]
https://updates.drupal.org/release-history/views/7.x
/home/nagios/.drush/cache/download/https---updates.drupal.org-release-history-views-7.x   [notice]
retrieved from cache.
advanced_forum,7.x-2.1,7.x-2.5,Update available
ctools,7.x-1.7,7.x-1.7,Up to date
panels,7.x-3.1,7.x-3.5,Update available
Command dispatch complete                                               [notice]
"""
REMOTE_DRUSH_CMD3_OUTPUT = r"""Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_SFVF1a --database=drupal --host=mysql --silent  < /tmp/drush_50OnWJ
The drush command 'pmlist' could not be found.  Run `drush               [error]
cache-clear drush` to clear the commandfile cache if you have
installed new extensions.
alignak@a556709624a8:/opt/drupalplugins/env/bin$ drush @drupal pml --format=csv 2>/dev/null
Initialized Drupal 7.37 root directory at /var/www/html                 [notice]
Initialized Drupal site drupal at sites/default                         [notice]
Executing: mysql --defaults-extra-file=/tmp/drush_KNBl1Z --database=drupal --host=mysql --silent  < /tmp/drush_TurZU8
Loading outputformat engine.                                            [notice]
Chaos tool suite,Bulk Export (bulk_export),Module,Not installed,7.x-1.7
Chaos tool suite,Chaos tools (ctools),Module,Enabled,7.x-1.7
Chaos tool suite,Chaos Tools (CTools) AJAX Example (ctools_ajax_sample),Module,Not installed,7.x-1.7
Chaos tool suite,Chaos Tools (CTools) Plugin Example (ctools_plugin_example),Module,Not installed,7.x-1.7
Chaos tool suite,Custom content panes (ctools_custom_content),Module,Not installed,7.x-1.7
Chaos tool suite,Custom rulesets (ctools_access_ruleset),Module,Not installed,7.x-1.7
Chaos tool suite,Page manager (page_manager),Module,Not installed,7.x-1.7
Chaos tool suite,Stylizer (stylizer),Module,Not installed,7.x-1.7
Chaos tool suite,Term Depth access (term_depth),Module,Not installed,7.x-1.7
Chaos tool suite,Views content panes (views_content),Module,Not installed,7.x-1.7
Core,Aggregator (aggregator),Module,Not installed,7.37
Core,Block (block),Module,Enabled,7.37
Core,Blog (blog),Module,Not installed,7.37
Core,Book (book),Module,Not installed,7.37
Core,Color (color),Module,Enabled,7.37
Core,Comment (comment),Module,Enabled,7.37
Core,Contact (contact),Module,Not installed,7.37
Core,Content translation (translation),Module,Not installed,7.37
Core,Contextual links (contextual),Module,Enabled,7.37
Core,Dashboard (dashboard),Module,Enabled,7.37
Core,Database logging (dblog),Module,Enabled,7.37
Core,Field (field),Module,Enabled,7.37
Core,Field SQL storage (field_sql_storage),Module,Enabled,7.37
Core,Field UI (field_ui),Module,Enabled,7.37
Core,File (file),Module,Enabled,7.37
Core,Filter (filter),Module,Enabled,7.37
Core,Forum (forum),Module,Enabled,7.37
Core,Help (help),Module,Enabled,7.37
Core,Image (image),Module,Enabled,7.37
Core,List (list),Module,Enabled,7.37
Core,Locale (locale),Module,Not installed,7.37
Core,Menu (menu),Module,Enabled,7.37
Core,Node (node),Module,Enabled,7.37
Core,Number (number),Module,Enabled,7.37
Core,OpenID (openid),Module,Not installed,7.37
Core,Options (options),Module,Enabled,7.37
Core,Overlay (overlay),Module,Enabled,7.37
Core,Path (path),Module,Enabled,7.37
Core,PHP filter (php),Module,Not installed,7.37
Core,Poll (poll),Module,Not installed,7.37
Core,RDF (rdf),Module,Enabled,7.37
Core,Search (search),Module,Enabled,7.37
Core,Shortcut (shortcut),Module,Enabled,7.37
Core,Statistics (statistics),Module,Not installed,7.37
Core,Syslog (syslog),Module,Not installed,7.37
Core,System (system),Module,Enabled,7.37
Core,Taxonomy (taxonomy),Module,Enabled,7.37
Core,Testing (simpletest),Module,Not installed,7.37
Core,Text (text),Module,Enabled,7.37
Core,Toolbar (toolbar),Module,Enabled,7.37
Core,Tracker (tracker),Module,Not installed,7.37
Core,Trigger (trigger),Module,Not installed,7.37
Core,Update manager (update),Module,Enabled,7.37
Core,User (user),Module,Enabled,7.37
Other,Advanced Forum (advanced_forum),Module,Enabled,7.x-2.1
Panels,Mini panels (panels_mini),Module,Not installed,7.x-3.1
Panels,Panel nodes (panels_node),Module,Not installed,7.x-3.1
Panels,Panels (panels),Module,Enabled,7.x-3.1
Panels,Panels In-Place Editor (panels_ipe),Module,Not installed,7.x-3.1
Views,Views (views),Module,Enabled,7.x-3.1
Views,Views UI (views_ui),Module,Not installed,7.x-3.1
Core,Bartik (bartik),Theme,Enabled,7.37
Core,Garland (garland),Theme,Disabled,7.37
Core,Seven (seven),Theme,Enabled,7.37
Core,Stark (stark),Theme,Disabled,7.37
Command dispatch complete                                               [notice]
"""
EXPECTED_OUTPUT_CRIT = r"""Drupal Core version;7.37;-1
Database system;MySQL, MariaDB, or equivalent;-1
DBMS version;5.6.25;-1
Database update;Up to date;-1
PHP version;5.6.9;-1
Enabled modules;4;-1
drupal;SECURITY UPDATE available;0
advanced_forum;Update available;1
panels;Update available;1
views;SECURITY UPDATE available;0"""

EXPECTED_OUTPUT_WARN = r"""Drupal Core version;7.37;-1
Database system;MySQL, MariaDB, or equivalent;-1
DBMS version;5.6.25;-1
Database update;Up to date;-1
PHP version;5.6.9;-1
Enabled modules;4;-1
advanced_forum;Update available;1
panels;Update available;1"""

EXPECTED_OUTPUT_OK = r"""Drupal Core version;7.37;-1
Database system;MySQL, MariaDB, or equivalent;-1
DBMS version;5.6.25;-1
Database update;Up to date;-1
PHP version;5.6.9;-1
Enabled modules;4;-1"""

FORCE_WARNING = False
FORCE_OK = False


def _call_site_audit_mock(self, args):
    cmd1 = set(['--json', '--detail', 'as'])
    cmd2 = set(['ups', '--format=csv'])
    cmd3 = set(['pml', '--format=csv'])

    args_set = set(args)

    if cmd1.issubset(args_set):
        if self.home:
            return REMOTE_DRUSH_CMD1_OUTPUT
        return LOCAL_DRUSH_CMD1_OUTPUT
    elif cmd2.issubset(args_set):
        if self.home:
            if FORCE_WARNING:
                return REMOTE_DRUSH_CMD2_OUTPUT_WARN
            elif FORCE_OK:
                return REMOTE_DRUSH_CMD2_OUTPUT_OK
            return REMOTE_DRUSH_CMD2_OUTPUT

        if FORCE_WARNING:
            return LOCAL_DRUSH_CMD2_OUTPUT_WARN
        elif FORCE_OK:
            return LOCAL_DRUSH_CMD2_OUTPUT_OK
        return LOCAL_DRUSH_CMD2_OUTPUT
    elif cmd3.issubset(args_set):
        if self.home:
            return REMOTE_DRUSH_CMD3_OUTPUT
        return LOCAL_DRUSH_CMD3_OUTPUT
    else:
        return None


class Testdrupal_status(TestPlugin):
    def setUp(self):
        global FORCE_WARNING
        global FORCE_OK
        FORCE_WARNING = False
        FORCE_OK = False
        Plugin._call_site_audit = _call_site_audit_mock

    def test_version(self):
        args = ["-v"]
        self.execute(Plugin, args, 0, stderr_pattern="version " + Plugin.VERSION)

    def test_help(self):
        args = ["-h"]
        self.execute(Plugin, args, 0, "usage:")

    def test_critical(self):
        args = ["-w", "140", "-c", "120", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT_CRIT)

    def test_warning(self):
        global FORCE_WARNING
        FORCE_WARNING = True
        args = ["-w", "110", "-c", "90", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT_WARN)

    def test_ok(self):
        global FORCE_OK
        FORCE_OK = True
        args = ["-w", "70", "-c", "40", "-p", "/var/www/html/"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT_OK)

    def test_remote_critical(self):
        args = ["-w", "140", "-c", "120", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 2, EXPECTED_OUTPUT_CRIT)

    def test_remote_warning(self):
        global FORCE_WARNING
        FORCE_WARNING = True
        args = ["-w", "110", "-c", "90", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 1, EXPECTED_OUTPUT_WARN)

    def test_remote_ok(self):
        global FORCE_OK
        FORCE_OK = True
        args = ["-w", "60", "-c", "30", "-a", "@drupal", "-d", "/home/alignak"]
        self.execute(Plugin, args, 0, EXPECTED_OUTPUT_OK)

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