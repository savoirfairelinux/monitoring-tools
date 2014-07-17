#!/bin/bash

rm -f env
virtualenv env
source env/bin/activate
pip install -I nose
pip install -r requirements.txt
nosetests
