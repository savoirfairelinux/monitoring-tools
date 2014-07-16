#!/bin/bash
set -e
export GREP_OPTIONS=""

for folder in `ls -d plugin-check-*/`; do
    cd $folder
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
