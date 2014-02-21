Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_http
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_http

or

::

  /usr/lib64/nagios/plugins/check_http

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 80 and/or 443 from Poller to monitored client
