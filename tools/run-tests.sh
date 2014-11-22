#!/bin/bash
set -e
export GREP_OPTIONS=""

# Setup a wheelhouse
[ ! -d /tmp/wheelhouse ] && mkdir /tmp/wheelhouse
pip wheel -w /tmp/wheelhouse lxml
pip wheel -w /tmp/wheelhouse nose
pip wheel -w /tmp/wheelhouse shinkenplugins

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

# finally: shinkenplugins
cd shinkenplugins
./run_tests.sh
cd ..
