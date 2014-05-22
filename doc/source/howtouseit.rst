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


