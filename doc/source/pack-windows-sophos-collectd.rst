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

.. include:: examples/collectd.confInstallation
============

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


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


