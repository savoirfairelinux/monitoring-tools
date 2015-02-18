#!/bin/bash

pip_install="pip install --use-wheel --find-links=file:///tmp/wheelhouse"

rm -rf env
virtualenv env
source env/bin/activate
$pip_install nose
$pip_install .
[ -f requirements.tests.txt ] && $pip_install -r requirements.tests.txt
(cd tests && nosetests) && rm -rf env
