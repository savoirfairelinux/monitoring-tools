Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

This pack will create services which need the following modules :

* Arbiter/Receiver : mod-collectd


Here an example of a arbiter-collectd module config file:

.. include:: examples/arbiter-collectd.cfg.example


Plugins
~~~~~~~

This pack will create services which need the following plugins :

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 25826 from monitored client to the Arbiter/Receiver Collectd module


Collectd
~~~~~~~~

Here an example of a collectd config file:

.. include:: examples/collectd.conf
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

* windows_collectd_counter.trig
* windows_collectd_counter_multiple.trig
* windows_collectd_cpu.trig
* windows_collectd_df.trig
* windows_collectd_disk.trig
* windows_collectd_interface.trig
* windows_collectd_memory.trig
* windows_collectd_memory-pagefile.trig
* windows-collectd_process.trig
* windows-collectd_processes.trig
* windows-collectd_service.trig
* windows-collectd_users.trig


