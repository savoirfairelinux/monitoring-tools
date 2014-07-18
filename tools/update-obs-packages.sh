#!/bin/bash

# first arg: name of the obs package
# second arg: path of the source files
function obs_push {
	# Checkout the package	
	osc co ${OBS_REPO}/$1

	# Calculate checksum of .dsc files
	OBS_CHECKSUM=$(shasum ${DIR}/${OBS_REPO}/$1/*.dsc | awk '{print $1}')
	CURRENT_CHECKSUM=$(shasum $2/$1*.dsc | awk '{print $1}')
	echo OBS CHECKSUM: $OBS_CHECKSUM
	echo CURRENT CHECKSUM: $CURRENT_CHECKSUM
	
	#Only update the files if the .dsc has changed.
	if [[ $OBS_CHECKSUM != $CURRENT_CHECKSUM ]]
	then
	# Remove the old files
	rm ${DIR}/${OBS_REPO}/$1/*

	# Copy the new files
	mv $2/$1*.tar.gz ${DIR}/${OBS_REPO}/$1/
	mv $2/$1*.dsc ${DIR}/${OBS_REPO}/$1/
	mv $2/$1*.changes ${DIR}/${OBS_REPO}/$1/
	
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
OBS_REPO=home:ReAzem:sfl-shinken-plugins

# plugins
for plugin in `(cd plugins && ls -d */ | tr -d '/')`
do
    obs_push $plugin plugins
done

# library
obs_push shinkenplugins .
