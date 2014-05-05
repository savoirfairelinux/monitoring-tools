Installation
============

On the poller side
-------------------
Setup the /etc/radiusclient-ng/radiusclient.conf and /etc/radiusclient-ng/servers files properly.

At least, you have to add a line into the servers file for your radius server. Don't forget to add the secret value!


On the radius server side
--------------------------

Setup the /etc/raddb/clients.conf and /etc/raddb/users files properly.
The clients.conf file is used to add the poller IP and set the secret value.
The users file is used to define user/password credentials



