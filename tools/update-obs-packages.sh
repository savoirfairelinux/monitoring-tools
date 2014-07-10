#!/bin/bash

#This is the sfl-shinken-plugins directory
DIR=$(pwd)

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

#Checkout the plugins
osc co home:ReAzem:sfl-shinken-plugins

for plugin in `ls  | grep plugin-`
do 
	#Copy the files
	mv ${DIR}/${plugin}*.tar.gz "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
	mv ${DIR}/${plugin}*.dsc "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
	mv ${DIR}/${plugin}*.changes "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
done

# Add the changes and commit everything
osc addremove home\:ReAzem\:sfl-shinken-plugins/plugin-*/*
osc ci home\:ReAzem\:sfl-shinken-plugins/ -m "Updated plugins"
