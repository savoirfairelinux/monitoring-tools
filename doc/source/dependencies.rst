Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_dhcp
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_tcp

or

::

  /usr/lib64/nagios/plugins/check_tcp


Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 4505 Poller to monitored client
