sfl-generic-repodeb-http
========================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_http
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_http

or

::

  /usr/lib64/nagios/plugins/check_http


Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 80 and 443 from Poller to monitored client

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_URI_REPO
----------

:type:              URI
:description:       The URI of the repo to check
