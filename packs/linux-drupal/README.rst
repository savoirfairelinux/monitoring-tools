sfl-linux-drupal
================

Dependencies
************

Plugins
~~~~~~~

This pack will create services which need the following plugins :

::

  /usr/lib/nagios/plugins/drupal_cache

::

  /usr/lib/nagios/plugins/drupal_codebase

::

  /usr/lib/nagios/plugins/drupal_cron

::

  /usr/lib/nagios/plugins/drupal_database

::

  /usr/lib/nagios/plugins/drupal_extensions

::

  /usr/lib/nagios/plugins/drupal_jenkins

::

  /usr/lib/nagios/plugins/drupal_logging

::

  /usr/lib/nagios/plugins/drupal_security

::

  /usr/lib/nagios/plugins/drupal_status

::

  /usr/lib/nagios/plugins/drupal_views

::

  /usr/lib/nagios/plugins/selenium

::

  /usr/lib/nagios/plugins/http_load



Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 22 from Poller to monitored client
* You can also use NRPE server

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition


_DRUPAL_OPTIONS
---------------

:type: command line arguments
:description: Pass arguments to drupal plugins. This way, you can choose between remote drush call or local drush

_JENKINS_OPTION
---------------

:type: command line arguments
:description: Pass arguments to jenkins plugins to set url, credentials, authentication endpoint, etc.

_DRUPAL_WARN
------------

:type: integer
:description: Drupal plugins warning treshold

_DRUPAL_CRIT
------------

:type: integer
:description: Drupal plugins critical treshold

_HTTP_LOAD_WARN
---------------

:type: float
:description: Http load plugins warning treshold

_HTTP_LOAD_CRIT
---------------

:type: float
:description: Http load plugins critical treshold

_HTTP_LOAD_OPTIONS
---------------

:type: command line arguments
:description: Pass arguments to http load plugin.

_SELENIUM_WARN
---------------

:type: integer
:description: Check selenium plugin warning treshold

_SELENIUM_CRIT
--------------

:type: integer
:description: Check selenium plugin critical treshold

_SELENIUM_PATH
--------------

:type: string
:description: Check selenium scenario path

_SELENIUM_SCENARIO
------------------

:type: string
:description: Check selenium scenario name without .py

