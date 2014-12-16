sfl-vmware-system-https
================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_vmware_api.pl
--------------------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_vmware_api.pl

or

  /usr/lib/64nagios/plugins/check_vmware_api.pl


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

_ESX_CPU_WARN
--------------

:type:              percent
:description:       Level for cpu usage


_ESX_CPU_CRIT
--------------

:type:              percent
:description:       Level for cpu usage


_ESX_MEM_WARN
--------------

:type:              percent
:description:       Level for ram usage


_ESX_MEM_CRIT
--------------

:type:              percent
:description:       Level for ram usage


_ESX_SWAP_WARN
--------------

:type:              percent
:description:       Level for swap usage


_ESX_SWAP_CRIT
--------------

:type:              percent
:description:       Level for swap usage


