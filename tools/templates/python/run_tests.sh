#!/bin/bash

rm -f env
virtualenv env
source env/bin/activate
pip install -I nose
pip install requirements.txt
nosetests
