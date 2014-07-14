#!/bin/bash
set -e
export GREP_OPTIONS=""

for folder in `ls -d plugin-*/`; do
    cd $folder
    ./test/jenkins/jenkins_unit_tests.sh
    cd ..
done
