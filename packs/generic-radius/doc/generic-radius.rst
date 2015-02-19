sfl-generic-radius
==================

Dependencies
************


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

Installation
************

On the poller side
-------------------
Setup the /etc/radiusclient-ng/radiusclient.conf and /etc/radiusclient-ng/servers files properly.

At least, you have to add a line into the servers file for your radius server. Don't forget to add the secret value!


On the radius server side
--------------------------

Setup the /etc/raddb/clients.conf and /etc/raddb/users files properly.
The clients.conf file is used to add the poller IP and set the secret value.
The users file is used to define user/password credentials



How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_RADIUSUSER
---------------

:type:              string
:description:       The Radius user login. Default: steve


_RADIUSPASSWORD
------------------

:type:              string
:description:       The Radius password login. Default: testing


_RADIUSFILE
------------

:type:              string
:description:       The Radius config file path. Default: /etc/radiusclient-ng/radiusclient.conf


_RADIUSPORT
------------

:type:              integer
:description:       The Radius udp port to query. Default: 1812