#!/bin/bash

wheel_house="/tmp/wheelhouse"

links="file://$wheel_house"

rm -rf env
virtualenv env
source env/bin/activate

pip install --upgrade pip nose setuptools wheel

pip wheel --find-links=${links} --wheel-dir=${wheel_house} .

pip install --use-wheel --find-links=${links} -e .[test]

(cd tests && nosetests) && rm -rf env
