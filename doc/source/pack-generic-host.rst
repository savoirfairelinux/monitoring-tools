Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_ping
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_ping

or

::

  /usr/lib64/nagios/plugins/check_ping

Network
~~~~~~~

This pack will create services which need the following protocol :

* ICMP

Installation
============

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
=============


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_LOAD_WARN
----------

:type:              3 comma-separated integer
:description:       Load warning threshold (ie: 7,6,5)


_LOAD_CRIT
----------

:type:              3 comma-separated integer",
:description:        Load critical threshold (ie: 10,9,8)"


_STORAGE_USED_WARN
------------------

:type:              percent
:description:       Warning level for used storage space


_STORAGE_USED_CRIT
------------------

:type:              percent
:description:       Critical level for used storage space


_PROCESS_CRON_MIN_WARN
----------------------

:type:              integer
:description:       Min number of cron processs, warning threshold



_PROCESS_RSYSLOGD_MIN_WARN
--------------------------

:type:              integer
:description:       Min number of rsyslog processs, warning threshold


_PROCESS_RSYSLOGD_MIN_CRIT
--------------------------

:type:              integer
:description:       Min number of rsyslog processs, critical threshold


_PROCESS_OSSEC_MIN_WARN
-----------------------

:type:              integer
:description:       Min number of ossec processs, warning threshold


_PROCESS_OSSEC_MIN_CRIT
-----------------------

:type:              integer
:description:       Min number of ossec processs, critical threshold


Triggers
~~~~~~~~

This is the list of triggers used in the pack :

* collectd_cpu.trig
* collectd_df.trig
* collectd_disk.trig
* collectd_interface.trig
* collectd_load.trig
* collectd_memory.trig
* collectd_processes.trig
* collectd_swap.trig
* collectd_users.trig


