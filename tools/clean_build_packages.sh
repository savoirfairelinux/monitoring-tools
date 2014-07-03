#!/bin/bash

DIR=$( cd "$( dirname "$0" )" && pwd )
cd $DIR
cd $DIR/../shinken-plugins-sfl/
rm -rf *.changes *.deb *.dsc *.tar.gz
