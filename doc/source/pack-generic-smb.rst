Dependencies
============


Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

check_samba
------------

This pack will create services which need the following plugin:

::

  /usr/lib/nagios/plugins/check_samba.py

or

::

  /usr/lib64/nagios/plugins/check_samba.py



Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 139 from Poller to monitored client
Installation
============

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)


How to use it
=============


Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_SMB_USER
----------

:type:              string
:description:       Samba user (Usally from AD). Default : $DOMAINUSERSHORT$


_SMB_PASSWORD
--------------

:type:              string
:description:       Samba password. Default : $DOMAINPASSWORD$


_SMB_DOMAIN
------------

:type:              string
:description:       Samba domain. Default : $DOMAIN$


_SMB_SHARED_DIR
------------------

:type:              string
:description:       Samba shared directory. Default : Documents


_SMB_TIME_WARN
---------------

:type:              integer
:description:       Samba time warning threshold (s). Default 3



_SMB_TIME_CRIT
--------------

:type:              integer
:description:       Samba time critical threshold (s). Default 5


_SMB_TIMEOUT
-------------

:type:              integer
:description:       Samba time before timeout (s). Default 10


