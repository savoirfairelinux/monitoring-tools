sfl-generic-ssh
===============

Dependencies
************


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

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_SSHPORT
--------

:type:              integer
:description:       SSH port. Usually 22

