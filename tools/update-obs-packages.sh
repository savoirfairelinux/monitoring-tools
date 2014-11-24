#!/bin/bash

# first arg: name of the obs package
# second arg: path of the source files
function obs_push {
    # Checkout the package
    osc co ${OBS_REPO}/$1

    # Check if the OBS orig and the current orig are different
    rm -rf /tmp/${1}_OBS_ORIG && mkdir /tmp/${1}_OBS_ORIG && tar -xf ${OBS_REPO}/${1}/${1}*.orig.tar.gz -C /tmp/${1}_OBS_ORIG --force-local
    diff -r ${2}/${1}/ /tmp/${1}_OBS_ORIG/${1}/ --exclude=debian --exclude=.git*

    #Only update the source has changed
    if [ $? -ne 0 ]; then
        echo Source has changed, uploading to obs...

        # Remove the old files
        rm ${DIR}/${OBS_REPO}/$1/*

        # Copy the new files
        mv $2/$1*.tar.gz ${DIR}/${OBS_REPO}/$1/
        mv $2/$1*.dsc ${DIR}/${OBS_REPO}/$1/
        mv $2/$1*.changes ${DIR}/${OBS_REPO}/$1/
        mv $2/$1*.diff.gz ${DIR}/${OBS_REPO}/$1/

        # Add the changes and commit
        osc addremove ${DIR}/${OBS_REPO}/$1/*
        osc ci ${DIR}/${OBS_REPO}/$1 -m "Updated ${1}"
    else
        echo Skipping OBS upload...
    fi
}


# This is the sfl-shinken-plugins directory
DIR=$(pwd)

# Open Build Service repository
OBS_REPO=home:sfl-monitoring:monitoring-tools

# plugins
for plugin in `(cd plugins && ls -d */ | tr -d '/')`
do
    obs_push $plugin plugins
done

# packs
for pack in `(cd packs && ls -d */ | tr -d '/')`
do
    obs_push $pack packs
done

# library
obs_push shinkenplugins .
