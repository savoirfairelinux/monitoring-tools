Monitoring Tools
================

[![Build Status](https://travis-ci.org/savoirfairelinux/monitoring-tools.svg?branch=master)](https://travis-ci.org/savoirfairelinux/monitoring-tools) [![Documentation Status](https://readthedocs.org/projects/sfl-monitoring-tools/badge/?version=latest&style)](https://readthedocs.org/projects/sfl-monitoring-tools/?badge=latest)

This repository contains plugins we use with Shinken, to check various
services, and which are not implemented in the usual plugins packages.

## Use

### Installation
The best way to install these plugins is through your package
manager. You can browse all the package repositories on
[Open Build Service project](https://build.opensuse.org/project/repositories/home:sfl-monitoring:monitoring-tools).


#### Debian
```
$ sudo sh -c "echo 'deb http://download.opensuse.org/repositories/home:/sfl-monitoring:/monitoring-tools/Debian_7.0/ ./' > /etc/apt/sources.list.d/monitoring-tools.list"
$ wget http://download.opensuse.org/repositories/home:/sfl-monitoring:/monitoring-tools/Debian_7.0/Release.key
$ sudo apt-key add - < Release.key
$ sudo apt-get update
$ sudo apt-get install plugin-<the plugin you want>
```

### Documentation
You can browse the online documentation at
http://sfl-monitoring-tools.readthedocs.org/

## Contribute

### Create a plugin
To generate a plugin, you need to install jinja2, either by pip or via
your package manager:
```
$ sudo pip install jinja2
```
or
```
$ sudo (apt-get|yum) install python-jinja2
```
Then
```
$ make new-plugin
```
To execute a plugin, you need to install the library
shinkenplugins:
```
$ sudo pip install shinkenplugins
```
or for Debian and Ubuntu:
```
$ sudo apt-get install lib-shinkenplugins
```

### Update the Debian packaging of a plugin/pack
After modifying files under debian/, you can add an entry in the
changelog by doing:
```
$ author=$(git log -n 1 --format=%aN)
$ export DEBFULLNAME=$author
$ email=$(git log -n 1 --format=%ae)
$ export DEBEMAIL=$email
$ msg=$(git log -n 1 --format=%s)
$ version=$(date +%Y.%m.%e.%H.%M)
$ dch $msg --no-auto-nmu --newversion $version
```    



### Build the Debian source packages
```
make packages
```
This will build the .orig.tar.gz, .debian.tar.gz, .dsc, and .changes files.


### Push the debian source packages to Open Build Service
```
make obs
```
This will checkout the OBS project and commit the new debian source
package files. You must be a maintainer on the OBS project to
successfully run this command. Travis has the permissions to do it.
