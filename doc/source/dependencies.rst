Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_dns
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_dns

or

::

  /usr/lib64/nagios/plugins/check_dns

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 53 and/or TCP 53 from Poller to monitored client
