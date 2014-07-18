#!/bin/bash

rm -rf env
virtualenv env --system-site-packages
source env/bin/activate
pip install -I nose
pip install -r requirements.txt
nosetests