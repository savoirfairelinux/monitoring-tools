#!/bin/sh
#
# 
#  Copyright (C) 2012 Savoir-Faire Linux Inc. 
# 
#  This program is free software; you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation; either version 3 of the License, or 
#  (at your option) any later version. 
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#  GNU General Public License for more details. 
#
#  You should have received a copy of the GNU General Public License 
#  along with this program; if not, write to the Free Software 
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA. 
#
#  Projects :
#            Shinken plugins
# 
#  File :
#            jenkins_tests.sh Script for Jenkins to launch tests
#
#
#  Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#

build_id=$1
# Delete old datas
rm -rf htmlcov
mkdir htmlcov -p
mkdir clover -p
# Prepare report
touch htmlcov/index.html
echo "<h2>Plugins list</h2>" > htmlcov/index.html
echo "<ul>" >> htmlcov/index.html
cd shinken-plugins-sfl
for i in `ls -1`
do
    echo "=========================================="
    echo "                  TEST                    "
    echo "        $i                                "
    echo "=========================================="
    cd $i
    git reset --hard
    git pull origin master
    test/jenkins/jenkins_unit_tests.sh
    prct=`cat test/total_coverage.txt`
    if [ -z $prct ]
    then
        prct=`grep -R covered test/htmlcov/index.html  -A 1 |grep Value |cut -d ">" -f 2 |cut -d "<" -f 1`
    fi
    echo "<li><a href=$i/index.html>$i</a> - $prct</li>" >> ../../htmlcov/index.html
    mv test/htmlcov ../../htmlcov/$i
    if [ -e cover_db ]
    then
        mv cover_db/clover.xml ../../clover/
    fi
    cd ..
    rm -rf last_env
    rm -rf last_env_hash
done
cd ..

echo "</ul>">> htmlcov/index.html

echo
echo "=========================================="
echo "=              Build Packages            ="
echo "=========================================="

#Get last version
rm -rf packages
mkdir packages
./tools/build_deb.sh
mv ../*.deb packages
mv libs/*.deb packages
mv shinken-plugins-sfl/*.deb packages
echo
echo "----------"
echo
./tools/build_rpm.sh
mv /home/jenkins/rpmbuild/RPMS/i386/*.rpm packages
mv /home/jenkins/rpmbuild/RPMS/x86_64/*.rpm packages

# clean
rm -f ../shinken-plugins-sfl_*.changes
rm -f ../shinken-plugins-sfl_*.tar.gz
rm -f ../shinken-plugins-sfl_*.dsc
rm -f ../shinken-plugins-sfl.tar.gz
rm -f shinken-plugins-sfl/*.changes
rm -f shinken-plugins-sfl/*.tar.gz
rm -f shinken-plugins-sfl/*.dsc
