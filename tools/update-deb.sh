#!/bin/bash

DIR=$(pwd)

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

# todo: set -e
# when we have all changelogs, etc

for plugin in `ls  | grep plugin-`
do 
	# Create the orig source tar
        # that's... temporary
        # timestamp=$(date +%s)
        # 2014 is used as long as we don't update original changelogs
	tar -czf ${plugin}_20140000.orig.tar.gz $plugin/ --exclude=${plugin}/debian/* --exclude=${plugin}/.git*
        
	# Build the package
	cd $DIR/$plugin
        author=$(git log -n 1 --format=%aN)
        export DEBFULLNAME=$author
        email=$(git log -n 1 --format=%ae)
        export DEBEMAIL=$email
        msg=$(git log -n 1 --format=%s)
        
        dch $msg --no-auto-nmu --newversion 20140000-1
        
	dpkg-buildpackage -us -uc -S --source-option=-Zgzip
        
        cd ..
done
