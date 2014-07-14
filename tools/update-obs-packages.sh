#!/bin/bash

#This is the sfl-shinken-plugins directory
DIR=$(pwd)

#Checkout the plugins
osc co home:ReAzem:sfl-shinken-plugins

#Remove the old files
rm ${DIR}/home:ReAzem:sfl-shinken-plugins/plugin-*/*

for plugin in `ls -d plugin-*/ | tr -d '/'`
do 
	#Copy the files
	mv ${DIR}/${plugin}*.tar.gz "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
	mv ${DIR}/${plugin}*.dsc "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
	mv ${DIR}/${plugin}*.changes "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
done

# Add the changes and commit everything
osc addremove home\:ReAzem\:sfl-shinken-plugins/plugin-*/*
osc ci home\:ReAzem\:sfl-shinken-plugins/ -m "Updated plugins"
