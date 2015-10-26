sfl-generic-rabbitmq-http
=========================

Dependencies
************

Plugins
~~~~~~~

This pack will create services which need the following plugins :

nagios-plugins-rabbitmq from https://github.com/jamesc/nagios-plugins-rabbitmq.git

Network
~~~~~~~

This pack will create services which need the following protocol :

HHTP/HTTPS port 15672 from poller to monitored rabbitmq.

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)

If you use this plugins directly from a poller, you will have to modify the default rabbitmq configuration.

Add the followin statement ::

  {loopback_users, []},

This will allow guest to be used from a remote host. Consider updating firewall rule in order to not expose this publicly

How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

RABBITMQ_USER
-------------

:type:              String
:description:       Rabbitmq admin user


_RABBITMQ_PASSWORD
------------------

:type:              String
:description:       Rabbitmq admin password


_QUEUES
-------

:type:              Comma separated String list
:description:       List of queues to monitor
