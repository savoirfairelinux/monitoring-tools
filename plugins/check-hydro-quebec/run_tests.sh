#!/bin/bash

wheel_house="/tmp/wheelhouse"

rm -rf env
virtualenv env
source env/bin/activate

pip install --upgrade pip nose setuptools wheel

pip wheel --find-links=${wheel_house} --wheel-dir=${wheel_house} .

pip install --use-wheel --find-links=${wheel_house} -e .[test]

(cd . && nosetests) && rm -rf env
