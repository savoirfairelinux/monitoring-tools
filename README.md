Shinken plugins
===============

[![Build Status](https://travis-ci.org/savoirfairelinux/sfl-shinken-plugins.svg?branch=master)](https://travis-ci.org/savoirfairelinux/sfl-shinken-plugins)

This repository contains plugins we use with Shinken, to check various
services, and which are not implemented in the usual plugins packages.

You can browse the online documentation at
http://sfl-shinken-plugins.readthedocs.org/en/latest/


#### Updating submodules
``` 
make update-submodules 
```
This will checkout all the submodules to master, update the documentation and create a new commit.


#### Building the debian source package files
```
make deb
```
This will build the .orig.tar.gz, .debian.tar.gz, .dsc, and .changes files.


#### Pushing the debian source package files to Open Build Service
```
make deb && make obs
```
This will checkout the OBS project and commit the new debian source package files. You must be a maintainer on the OBS project to successfully run this command. Travis has the permissions to do it.
