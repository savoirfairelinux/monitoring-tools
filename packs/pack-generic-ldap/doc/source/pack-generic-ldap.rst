pack-generic-ldap
================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_ldap
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_ldap

or

::

  /usr/lib64/nagios/plugins/check_ldap

check_ldaps
-----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_ldaps

or

::

  /usr/lib64/nagios/plugins/check_ldaps

check_tcp
-----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_tcp

or

::

  /usr/lib64/nagios/plugins/check_tcp


Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 636 from Poller to monitored client with SSL
* TCP 389 from Poller to monitored client without SSL


Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Templates
~~~~~~~~~

generic-ldap
~~~~~~~~~~~~

Use this template to monitoring a standard LDAP server.

generic-ldap3
~~~~~~~~~~~~~

Use this template to monitoring a LDAP3 server.

generic-ldaps
~~~~~~~~~~~~~

Use this template to monitoring a LDAPS server.


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_LDAPBASE
---------

:type:              string
:description:       The read snmp community allowed on the linux server

_DOMAIN
-------

:type:              string
:description:       The read snmp community allowed on the linux server

_DOMAINUSERSHORT
----------------

:type:              string
:description:       Short name (without the domain) of the user to query the server. Should have rights on the WMI tables for reading

_DOMAINUSER
-----------

:type:              string
:description:       Full name of the user to query. Is by default DOMAIN\\USERSHORT

_DOMAINPASSWORD
---------------

:type:              string
:description:       Password for the user that will launch the query

Triggers
~~~~~~~~

