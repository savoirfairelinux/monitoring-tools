Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_ssh
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_ssh

or

::

  /usr/lib64/nagios/plugins/check_ssh


Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 22 from Poller to monitored client
