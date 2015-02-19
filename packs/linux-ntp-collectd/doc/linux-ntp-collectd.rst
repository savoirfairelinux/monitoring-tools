sfl-linux-ntp-collectd
======================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

This pack will create services which need the following modules :

* Arbiter/Receiver : mod-collectd

Plugins
~~~~~~~

This pack will create services which need the following plugins :

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 25826 from monitored client to the Arbiter/Receiver Collectd module
Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_TIME_OFFSET_WARN
----------------------

:type:              integer
:description:       offset warning threshold



_TIME_OFFSET_CRIT
--------------------------

:type:              integer
:description:       offset critical threshold


_TIME_DISPERSION_WARN
--------------------------

:type:              integer
:description:       dispersion warning threshold


_TIME_DISPERSION_CRIT
-----------------------

:type:              integer
:description:       dispersion critical threshold



Triggers
~~~~~~~~

This is the list of triggers used in the pack :

* collectd_ntpd.trig

