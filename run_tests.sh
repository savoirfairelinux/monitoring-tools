#!/bin/bash

for folder in `ls -d plugin-*`; do
    cd $folder
    ./test/jenkins/jenkins_unit_tests.sh
done
