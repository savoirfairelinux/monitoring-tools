How to use it
=============


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_MSSQL_SOPHOS_INSTANCES
------------------------

:type:              Comma separated string list
:description:       MSSQL Instances for Sophos. Default : SOPHOS (only one element)

_PROCESS_SOPHOS_MIN_WARN
----------------------

:type:              integer
:description:       Min number of Sophos processes, warning threshold


_PROCESS_SOPHOS_MIN_CRIT
----------------------

:type:              integer
:description:       Min number of Sophos processes, critical threshold

Triggers
~~~~~~~~

This is the list of triggers used in the pack :

* windows_collectd_service.trig
* windows_collectd_processes.trig


