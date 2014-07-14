Shinken plugins
===============

[![Build Status](https://travis-ci.org/savoirfairelinux/sfl-shinken-plugins.svg?branch=master)](https://travis-ci.org/savoirfairelinux/sfl-shinken-plugins)

This repository contains plugins we use with Shinken, to check various
services, and which are not implemented in the usual plugins packages.

## Use

### Documentation
You can browse the online documentation at
http://sfl-shinken-plugins.readthedocs.org/en/latest/

### Debian packages

Debian repositories for all the plugins are found at the
[Open Build Service project](https://build.opensuse.org/project/repositories/home:ReAzem:sfl-shinken-plugins).

## Contribute

### Add a plugin
Fill me.

### Update the Debian packaging of a plugin
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

### Update submodules
```
make update-submodules 
```
This will checkout all the submodules to master, update the
documentation and create a new commit.


### Build the Debian source packages
```
make deb
```
This will build the .orig.tar.gz, .debian.tar.gz, .dsc, and .changes files.


### Push the debian source packages to Open Build Service
```
make deb && make obs
```
This will checkout the OBS project and commit the new debian source
package files. You must be a maintainer on the OBS project to
successfully run this command. Travis has the permissions to do it.
