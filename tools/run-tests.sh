#!/bin/bash
set -e
export GREP_OPTIONS=""


wheel_house="/tmp/wheelhouse"

# Setup a wheelhouse
mkdir -p "$wheel_house"

w="pip wheel --find-links=file://${wheel_house} -w ${wheel_house}"
$w lxml
$w pysnmp
$w nose
$w shinkenplugins


not_tested=""

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
        if test -x run_test.sh
        then
            ./run_tests.sh
        else
            echo "WARNING: $plugin not tested"
            not_tested="${not_tested}\n${plugin}"
        fi
    fi
    cd ..
done
cd ..

# finally: shinkenplugins
cd libs
for lib in `ls -d */`
do
    cd $lib
    if test -x run_test.sh
    then
        ./run_tests.sh
    else
        echo "WARNING: $lib not tested"
        not_tested="${not_tested}\n${lib}"
    fi
    cd ..
done
cd ..


if test "$not_tested"
then
    echo -e $(cat << END
===============================================
WARNING WARNING following libs were NOT tested:
$not_tested
===============================================
END
)
fi
