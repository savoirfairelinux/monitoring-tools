sfl-windows-rdp
================

Dependencies
************

Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_x224
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_x224

or

::

  /usr/lib64/nagios/plugins/check_x224



Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 3389 from Poller to monitored client

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

