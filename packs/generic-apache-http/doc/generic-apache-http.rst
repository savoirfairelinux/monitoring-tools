sfl-generic-apache-http
==========================

Dependencies
************

Plugins
~~~~~~~

check_apache_server_status
--------------------------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_apache_server_status

or

::

  /usr/lib64/nagios/plugins/check_apache_server_status

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 80 and 443 from Poller to monitored client

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_APACHEURL
----------

:type:              string
:description:       The apache status  path on server. Default: server-status

