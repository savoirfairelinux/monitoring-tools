Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

This pack will create services which need the following modules :

* Arbiter/Receiver : mod-collectd


Here an example of a arbiter-collectd module config file:

.. include:: examples/arbiter-collectd.cfg


Plugins
~~~~~~~

This pack will create services which need the following plugins :

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 25826 from monitored client to the Arbiter/Receiver Collectd module


Collectd
~~~~~~~~

Here an example of a collectd config file:

.. include:: examples/collectd.conf