Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_radius
-------------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_radius

or

::

  /usr/lib64/nagios/plugins/check_radius


Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP : 1645 or 1812 from Poller to monitored client
