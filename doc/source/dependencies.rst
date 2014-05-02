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

  /usr/lib/nagios/plugins/check_dhcp

or

::

  /usr/lib64/nagios/plugins/check_dhcp

The plugin permissions should be:

::

  -rwsr-xr-x root root check_dhcp

If not, you can fix it with

  sudo chown root: /usr/lib/nagios/plugins/check_dhcp
  sudo chmod u+s /usr/lib/nagios/plugins/check_dhcp

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 67 and 68 from Poller to monitored client
