#!/bin/bash

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

set -e

for plugin in `ls -d plugin-check-*/ | tr -d '/'`
do 
    # We extract the last version from the changelog
    version=$(cat $plugin/debian/changelog  | grep 'check-' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
    
    # We create the upstream source, foo.orig.tar.gz
    tar -czf ${plugin}_${version}.orig.tar.gz $plugin/ --exclude=${plugin}/debian/* --exclude=${plugin}/.git*
    
    # And let's build the source package
    cd $plugin
    dpkg-buildpackage -us -uc -S --source-option=-Zgzip
    cd ..
done
