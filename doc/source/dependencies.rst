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

* TCP and UDP : 1645, 1646, 1812, 1813 from Poller to monitored client
