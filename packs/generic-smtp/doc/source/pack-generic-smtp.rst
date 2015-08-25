sfl-generic-smtp
=========================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_smtp
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_smtp

or

::

  /usr/lib64/nagios/plugins/check_smtp

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 25

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_SMTPWARN
--------------

:type:              Integer
:description:       Warning threshold. Default: 3

_SMTPCRIT
--------------

:type:              Integer
:description:       Critical threshold. Default: 5
