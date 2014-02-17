How to use it
=============


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

