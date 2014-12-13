pack-linux-system-nrpe
================

Dependencies
************


Shinken Modules
~~~~~~~~~~~~~~~

This pack will create services which need the following modules :

* Poller: mod-booster-nrpe

Here an example of a booster-nrpe module config file:

.. include:: examples/booster_nrpe.cfg.example

Plugins
~~~~~~~

This pack will create services which need the following plugins :

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 5666 from Poller to  monitored client

NRPE
~~~~~~~~

Here an example of a nrpe config file (in /etc/nagios/nrpe.d/):

.. include:: examples/linux-system-nrpe_local.cfg.example

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

Triggers
~~~~~~~~

