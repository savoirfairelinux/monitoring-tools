Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_samba
------------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_samba.py

or

::

  /usr/lib64/nagios/plugins/check_samba.py



Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 139 from Poller to monitored client
