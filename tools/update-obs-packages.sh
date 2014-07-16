#!/bin/bash

#This is the sfl-shinken-plugins directory
DIR=$(pwd)

# Open Build Service repository
OBS_REPO=home:ReAzem:sfl-shinken-plugins

#Checkout the plugins
osc co ${OBS_REPO}

#Remove the old files
rm ${DIR}/${OBS_REPO}/plugin-*/*

# library + plugins
# the library is found by ls thanks to the leading wildcard
for plugin in `ls -d *plugin*/ | tr -d '/'`
do 
	#Copy the files
	mv ${DIR}/${plugin}*.tar.gz ${DIR}/${OBS_REPO}/${plugin}/
	mv ${DIR}/${plugin}*.dsc ${DIR}/${OBS_REPO}/${plugin}/
	mv ${DIR}/${plugin}*.changes ${DIR}/${OBS_REPO}/${plugin}/
	
	# Add the changes and commit
	osc addremove ${DIR}/${OBS_REPO}/${plugin}/*
	osc ci ${DIR}/${OBS_REPO}/${plugin} -m "Updated plugins"
done


