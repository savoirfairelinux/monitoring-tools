#!/bin/bash

rm -rf env
virtualenv env
source env/bin/activate
pip install --use-wheel --find-links=file:///tmp/wheelhouse -I nose
[ -f requirements.tests.txt ] && pip install --use-wheel --find-links=/tmp/wheelhouse -r requirements.tests.txt
pip install --use-wheel --find-links=file:///tmp/wheelhouse -r requirements.txt
nosetests && rm -rf env
