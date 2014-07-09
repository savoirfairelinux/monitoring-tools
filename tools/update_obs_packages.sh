#!/bin/bash

#This is the sfl-shinken-plugins directory
DIR=$(pwd)

#Checkout the plugins
#osc co home:ReAzem:sfl-shinken-plugins

for plugin in `ls  | grep plugin-`
do 
	#Create the orig source tar
	date=$(cat $DIR/$plugin/debian/changelog  | grep 'check-' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
	tar -czf $DIR/${plugin}_${date}.orig.tar.gz $DIR/$plugin --exclude=${plugin}/debian/* --exclude=${plugin}/.git* --exclude=${plugin}/test
	#Build the package
	cd $DIR/$plugin
        author=$(git log -n 1 --format=%aN)
        export DEBFULLNAME=$author
        email=$(git log -n 1 --format=%ae)
        export DEBEMAIL=$email
        msg=$(git log -n 1 --format=%s)
        
        dch $msg --no-auto-nmu
        
	dpkg-buildpackage -us -uc -S

	#Copy the files
	#mv ${DIR}/${plugin}*.tar.gz "${DIR}/home:ReAzem:sfl-shinken-plugins/${plugin}/"
done

# Add the changes and commit everything
#cd ${DIR}
#osc add home\:ReAzem\:sfl-shinken-plugins/plugin-*/*
#osc ci home\:ReAzem\:sfl-shinken-plugins/ -m "Update plugins"
