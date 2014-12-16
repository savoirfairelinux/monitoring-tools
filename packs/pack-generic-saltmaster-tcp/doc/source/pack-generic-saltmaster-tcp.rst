sfl-generic-saltmaster-tcp
================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_dhcp
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_tcp

or

::

  /usr/lib64/nagios/plugins/check_tcp


Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 4505 Poller to monitored client

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition


_SALTMASTERPORT
----------------

:type:              integer
:description:       Salt master port. Default 4505


_TIME_WARN
------------------

:type:              double
:description:       Response time warning threshold. Default 1


_TIME_CRIT
------------------

:type:              double
:description:       Response time critical threshold. Default 2


