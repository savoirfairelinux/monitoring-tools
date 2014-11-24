#!/bin/bash

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

set -e

# -S builds only the source package, the binary one is done by OpenBuildService
# --ignore-bad-version skips the date check, because the files can be more recent
# than the last debian/changelog entry
BUILD_PACKAGE="dpkg-buildpackage -us -uc -S --source-option=-Zgzip --source-option=--ignore-bad-version"

# library package
# We extract the last version from the changelog
version=$(cat shinkenplugins/debian/changelog  | grep 'shinkenplugins' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
tar -czf shinkenplugins_${version}.orig.tar.gz shinkenplugins/ --exclude=$shinkenplugins/debian/*
cd shinkenplugins
$BUILD_PACKAGE || true
cd ..

# plugin packages
cd plugins
for plugin in `ls -d */ | tr -d '/'`
do 
    # We extract the last version from the changelog
    version=$(cat $plugin/debian/changelog  | grep 'check-' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
    
    # We create the upstream source, foo.orig.tar.gz
    tar -czf ${plugin}_${version}.orig.tar.gz $plugin/ --exclude=${plugin}/debian/* --exclude=${plugin}/.git*
    
    # And let's build the source package
    cd $plugin
    $BUILD_PACKAGE || true
    cd ..
done
cd ..

# pack packages
cd packs
for pack in `ls -d */ | tr -d '/'`
do
    # Extract last version number
    version=$(cat $pack/debian/changelog | grep 'pack-' | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)

    # Create the "upstream source" archive
    # If the directory contains a collectd directory: exclude it
    tar -czf ${pack}_${version}.orig.tar.gz $pack/ --exclude=${pack}/debian/* --exclude=${pack}/.git*

    # Build the source package
    cd $pack
    dpkg-buildpackage -us -uc -S --source-option=-Zgzip --source-option=--ignore-bad-version --source-option=-Icollectd || true
    cd ..

done
