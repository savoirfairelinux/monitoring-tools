#!/bin/bash

# first arg: name of the obs package
# second arg: path of the files
function obs_push {
	# Copy the files
	mv $2*.tar.gz ${DIR}/${OBS_REPO}/$1/
	mv $2*.dsc ${DIR}/${OBS_REPO}/$1/
	mv $2*.changes ${DIR}/${OBS_REPO}/$1/

	# Add the changes and commit
	osc addremove ${DIR}/${OBS_REPO}/$1/*
	osc ci ${DIR}/${OBS_REPO}/$1 -m "Updated ${2}"
}


# This is the sfl-shinken-plugins directory
DIR=$(pwd)

# Open Build Service repository
OBS_REPO=home:ReAzem:sfl-shinken-plugins

# Checkout the plugins
osc co ${OBS_REPO}

# Remove the old files
rm ${DIR}/${OBS_REPO}/*/*

# plugins
for plugin in `(cd plugins && ls -d */ | tr -d '/')`
do
    obs_push $plugin plugins/$plugin
done

# library
obs_push shinkenplugins shinkenplugins
