#!/bin/bash

rm -rf env
virtualenv env
source env/bin/activate
pip install -f /tmp/wheelhouse -I nose
[ -f requirements.tests.txt ] && pip install -f /tmp/wheelhouse -r requirements.tests.txt
pip install -f /tmp/wheelhouse -r requirements.txt
nosetests && rm -rf env