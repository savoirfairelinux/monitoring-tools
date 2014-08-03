#!/bin/bash
set -e
export GREP_OPTIONS=""

# Plugins
cd plugins
for plugin in `ls -d */`; do
    cd $plugin
    file="./test/jenkins/jenkins_unit_tests.sh"
    # workaround, as long as we still have these dirty jenkins scripts
    if [ -e $file ]
    then
        $file
    else
        ./run_tests.sh
    fi
    cd ..
done
cd ..

# shinkenplugins
cd shinkenplugins
./run_tests.sh
cd ..
