sfl-windows-mssql
=================

Dpendencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_dhcp
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_mssql_health

or

::

  /usr/lib64/nagios/plugins/check_mssql_health


This plugin is available here : http://labs.consol.de/lang/en/nagios/check_mssql_health/

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 1433 from Poller to monitored client

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_MSSQL_CONNECTION_CRIT
-------------------------

:type:              string
:description:       Time to connect to the server

_MSSQL_CONNECTION_WARN
-------------------------


:type:              string
:description:       Time to connect to the server

_MSSQL_CONNECTED_USERS_CRIT
-------------------------


:type:              string
:description:       Number of currently connected users

_MSSQL_CONNECTED_USERS_WARN
-------------------------


:type:              string
:description:       Number of currently connected users

_MSSQL_CPU_BUSY_CRIT
-------------------

:type:              percent
:description:       Cpu busy in percent

_MSSQL_CPU_BUSY_WARN
--------------------

:type:              percent
:description:       Cpu busy in percent

_MSSQL_IO_BUSY_CRIT
------------------


:type:              percent
:description:       IO busy in percent

_MSSQL_IO_BUSY_WARN
-------------------

:type:              percent
:description:       IO busy in percent

_MSSQL_FULL_SCANS_CRIT
----------------------

:type:              string
:description:       Full table scans per second

_MSSQL_FULL_SCANS_WARN
----------------------

:type:              string
:description:       Full table scans per second

_MSSQL_TRANSACTIONS_CRIT
------------------------

:type:              string
:description:       Transactions per second per database

_MSSQL_TRANSACTIONS_WARN
------------------------

:type:              string
:description:       Transactions per second per database

_MSSQL_BATCH_REQUESTS_CRIT
-------------------------

:type:              string
:description:       Batch requests per second

_MSSQL_BATCH_REQUESTS_WARN
--------------------------

:type:              string
:description:       Batch requests per second


Triggers
~~~~~~~~

