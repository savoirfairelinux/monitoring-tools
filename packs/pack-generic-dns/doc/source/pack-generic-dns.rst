sfl-generic-dns
================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_dns
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_dns

or

::

  /usr/lib64/nagios/plugins/check_dns

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 53 and/or TCP 53 from Poller to monitored client

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

_DNSHOSTNAME
------------

:type:          string
:description:   Hostname to resolve

_DNSEXPECTEDRESULT
------------------

:type:          string
:description:   Address expected returned by the DNS server

_DNSWARN
--------

:type:          Integer
:description:   Warning threshold

_DNSCRIT
--------

:type:          Integer
:description:   Critical threshold

Triggers
~~~~~~~~

No trigger used with this pack
