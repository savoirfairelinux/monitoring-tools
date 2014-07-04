Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_dhcp
----------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_dhcp

or

::

  /usr/lib64/nagios/plugins/check_dhcp

The plugin permissions should be:

::

  -rwsr-xr-x root root check_dhcp

If not, you can fix it with

  sudo chown root: /usr/lib/nagios/plugins/check_dhcp
  sudo chmod u+s /usr/lib/nagios/plugins/check_dhcp

Network
~~~~~~~

This pack will create services which need the following protocol :

* UDP 67 and 68 from Poller to monitored client

Installation
============

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
=============


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_SPLUNKAPACHE
--------------

:type:              string
:description:       IP of apache server where splunk is. Used if splunk is behind a Apache auth


_SPLUNKURL
----------

:type:               string
:description:        Splunk url on the webserver


_SPLUNKUSER
------------------

:type:              string
:description:       Splunk password


_SPLUNKPASSWORD
------------------

:type:              string
:description:       Splunk user password


_SPLUNKWARN
--------------

:type:              integer
:description:       Response time warning threshold



_SPLUNKCRIT
--------------------

:type:              integer
:description:       Response time warning threshold


