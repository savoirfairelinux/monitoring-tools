#!/bin/bash
set -e
export GREP_OPTIONS=""


wheel_house="/tmp/wheelhouse"

# Setup a wheelhouse
mkdir -p "$wheel_house"

w="pip wheel --find-links=${wheel_house} -w ${wheel_house}"
$w lxml
$w pysnmp
$w nose
$w shinkenplugins

# Plugins
cd plugins
for plugin in `ls -d */`; do
    echo "===============>>> $plugin <<<==============="
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
cd libs
for lib in `ls -d */`
do
    cd $lib
    ./run_tests.sh
    cd ..
done
cd ..
