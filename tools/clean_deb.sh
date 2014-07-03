#!/bin/bash

echo Clean all deb generated files
echo

DIR=$( cd "$( dirname "$0" )" && pwd )

rm -f $DIR/../shinken-plugins-sfl/*.{gz,deb,changes,dsc}
rm -f $DIR/../libs/*.{gz,deb,changes,dsc}

echo done
