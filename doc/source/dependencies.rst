Dpendencies
============


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

  /usr/lib/64nagios/plugins/check_mssql_health


This plugin is available here : http://labs.consol.de/lang/en/nagios/check_mssql_health/

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 1433 from Poller to monitored client
