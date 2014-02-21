Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_vmware_api.pl
--------------------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_vmware_api.pl

or

  /usr/lib/64nagios/plugins/check_vmware_api.pl


Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 80 and 443 from Poller to monitored client
