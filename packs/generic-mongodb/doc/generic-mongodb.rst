sfl-generic-mongodb
===================

Dependencies
************

Shinken Modules
~~~~~~~~~~~~~~~

Plugins
~~~~~~~

This pack will create services which need the following plugin :

https://github.com/mzupan/nagios-plugin-mongodb/blob/master/check_mongodb.py

and it here:

`/usr/lib/nagios/plugins/check_mongodb.py`

Network
~~~~~~~

This pack will create services which need the following protocol :

* TCP 27017 to connect with MongoDB
* SSL

Installation
************

Copy the pack folder in the packs folder defined in shinken.cfg (`cfg_dir=packs`)

How to use it
*************

Settings
~~~~~~~~

This is the list of settings which can be redefined in the host definition

_MONGO_PORT
-----------

:type:              integer
:description:       port of Mongodb
:default:           27017

_MONGO_CONNECTION_WARNING
-------------------------

:type:              integer
:description:       warning threshold for the connection time to the server
:default:           2

_MONGO_CONNECTION_CRITICAL
--------------------------

:type:              integer
:description:       critical threshold for the connection time to the server
:default:           4

_MONGO_PERCENTAGE_CONNECTION_WARNING
------------------------------------

:type:              integer
:description:       warning threshold for the connection pool
:defaut:            70

_MONGO_PERCENTAGE_CONNECTION_CRITICAL
-------------------------------------

:type:              integer
:description:       critical threshold for the connection pool
:defaut:            80

_MONGO_REPLICATION_LAG_WARNING
------------------------------

:type:              integer
:description:       warninig threshold for the lag : second
:defaut:            15

_MONGO_REPLICATION_LAG_CRITICAL
-------------------------------

:type:              integer
:description:       critical threshold for the lag : second
:defaut:            30

_MONGO_REPLICATION_LAG_PERCENT_WARNING
--------------------------------------

:type:              integer
:description:       warning threshold for the lag
:defaut:            50

_MONGO_REPLICATION_LAG_PERCENT_CRITICAL
---------------------------------------

:type:              integer
:description:       critical threshold for the lag
:defaut:            75

_MONGO_MEMORY_WARNING
---------------------

:type:              integer
:description:       warning threshold for usage of ram by MongoDB : gig
:defaut:            20

_MONGO_MEMORY_CRITICAL
----------------------

:type:              integer
:description:       critical threshold for usage of ram by MongoDB : gig
:defaut:            28

_MONGO_MEMORY_MAPPED_WARNING
----------------------------

:type:              integer
:description:       warning threshold for memory mapped : gig
:defaut:            20

_MONGO_MEMORY_MAPPED_CRITICAL
-----------------------------

:type:              integer
:description:       critical threshold for memory mapped : gig
:defaut:            28

_MONGO_LOCK_WARNING
-------------------

:type:              integer
:description:       warning threshold for the lock time : %
:defaut:            5

_MONGO_LOCK_CRITICAL
--------------------

:type:              integer
:description:       critical threshold for the lock time : %
:defaut:            10

_MONGO_FLUSHING_WARNING
-----------------------

:type:              integer
:description:       warning threshold for the average flush time : ms
:defaut:            100

_MONGO_FLUSHING_CRITICAL
------------------------

:type:              integer
:description:       critical threshold for the average flush time : ms
:defaut:            200

_MONGO_LAST_FLUSH_WARNING
-------------------------

:type:              integer
:description:       warning threshold for the last flush time : ms
:defaut:            200

_MONGO_LAST_FLUSH_CRITICAL
--------------------------

:type:              integer
:description:       critical threshold for the last flush time : ms
:defaut:            400

_MONGO_INDEX_MISS_RATIO_WARNING
-------------------------------

:type:              float
:description:       warning threshold for the ratio of index hits to misses
:defaut:            .005

_MONGO_INDEX_MISS_RATIO_CRITICAL
--------------------------------

:type:              float
:description:       critical threshold for the ratio of index hits to misses
:defaut:            .01

_MONGO_QUERIES_PER_SECOND_WARNING
---------------------------------

:type:              integer
:description:       warning threshold for the count of queries
:defaut:            200

_MONGO_QUERIES_PER_SECOND_CRITICAL
----------------------------------

:type:              integer
:description:       critical threshold for the count of queries
:defaut:            150

_MONGO_CONNECT_PRIMARY_WARNING
------------------------------

:type:              integer
:description:       warning threshold for the connection to the primary server of current replicaset : second
:defaut:            2

_MONGO_CONNECT_PRIMARY_CRITICAL
-------------------------------

:type:              integer
:description:       critical threshold for the connection to the primary server of current replicaset : second
:defaut:            4
