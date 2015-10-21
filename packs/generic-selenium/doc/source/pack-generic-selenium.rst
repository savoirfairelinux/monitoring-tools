sfl-generic-selenium
=========================

Dependencies
************

python-selenium >= 2.46.0

Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_selenium
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_selenium

or

::

  /usr/lib64/nagios/plugins/check_selenium

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 4444 from Poller to selenium-remote node. 

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
*************


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

