#!/bin/bash
echo build RPM Package
echo 

build_id=$1
git_hash=$2
rpmbuild=`which rpmbuild`

if [ -z $rpmbuild ]
then
    echo "rpmbuild not found. Please install rpm/rpmbuild"
    exit 1
fi

# Set variables
date=`date +%Y%m%d`
DIR=$( cd "$( dirname "$0" )" && pwd )
spec_file=$DIR/../shinken-plugins-sfl.spec
raw_message=`git log --format=%s |head -1`
date2=`date "+%a %b %d %Y"`
message="%changelog\n* $date2 Thibault Cohen <thibault.cohen@savoirfairelinux.com>\n- $raw_message\n"

# Prepare version
version=$(cat $spec_file | grep "^%define version     $date$" > /dev/null; echo $?)
if [ $version == '0' ]; then
    release=`grep "^%define release     [0-9]*$" $spec_file | awk '{print $NF}'`
    release=$(( $release + 1 ))
    sed -i "s/^%define release     .*$/%define release     $release/" $spec_file
else
    sed -i "s/^%define version     .*$/%define version     $date/" $spec_file
    sed -i "s/^%define release     .*$/%define release     1/" $spec_file
fi

# Create tar
#tar czf $DIR/../../shinken-plugins-sfl.tar.gz $DIR/../../shinken-plugins-sfl
# Copy tar to rpm folder
#cp $DIR/../../shinken-plugins-sfl.tar.gz ~/rpmbuild/SOURCES/
# Build
#rpmbuild -ba $spec_file --target x86_64 --define 'dist suse'
#rpmbuild -ba $spec_file --target i386 --define 'dist suse'
#rpmbuild -ba $spec_file --target x86_64 --define 'dist redhat'
#rpmbuild -ba $spec_file --target i386 --define 'dist redhat'

echo
echo "!!! BUILD NRPE static package !!!"
echo
cd $DIR/../nrpe
tar xzf nrpe-*.tar.gz
nrpe_source=`find . -name "nrpe-*.tar.gz" |grep -v static`
version=${nrpe_source//.\/nrpe-/}
version=${version//.tar.gz/}
rm -rf nrpe-static-sfl_*
rm -rf nrpe-$version
rm -f *.changes
rm -f *.dsc

patch -p0 < static-sfl.patch
mv nrpe-$version nrpe-static-sfl-$version
cp nrpe.cfg nrpe_local.cfg nrpe-static-sfl-$version
tar czf nrpe-static-sfl-$version.tar.gz nrpe-static-sfl-$version
mv nrpe-static-sfl-$version.tar.gz ~/rpmbuild/SOURCES/
spec_file=nrpe-static-sfl.spec
rpmbuild -ba $spec_file --target x86_64 --define 'dist suse'
rpmbuild -ba $spec_file --target i386 --define 'dist suse'
rpmbuild -ba $spec_file --target x86_64 --define 'dist redhat'
rpmbuild -ba $spec_file --target i386 --define 'dist redhat'

echo
echo "!!! BUILD libs packages !!!"
echo

cd $DIR/../libs/
for lib_name in `ls -l | egrep '^d' | awk '{print $NF}'`
do
  echo
  echo "!!!! BUILD $lib_name plugin package !!!!"
  echo
  lib=${lib_name//_/-}
  tar czf $lib.tar.gz $lib
  cp $lib.tar.gz ~/rpmbuild/SOURCES/
  spec_file=$lib_name/$lib_name.spec
  rpmbuild -ba $spec_file --target x86_64 --define 'dist suse'
  rpmbuild -ba $spec_file --target i386 --define 'dist suse'
  rpmbuild -ba $spec_file --target x86_64 --define 'dist redhat'
  rpmbuild -ba $spec_file --target i386 --define 'dist redhat'
done

echo
echo "!!! BUILD plugins packages !!!"
echo

cd $DIR/../shinken-plugins-sfl/
for plugin_name in `ls -l | egrep '^d' | awk '{print $NF}'`
do
  echo
  echo "!!!! BUILD $plugin_name plugin package !!!!"
  echo
  plugin=${plugin_name//_/-}
  tar czf $plugin.tar.gz $plugin_name
  cp $plugin.tar.gz ~/rpmbuild/SOURCES/
  spec_file=$plugin_name/$plugin_name.spec
  rpmbuild -ba $spec_file --target x86_64 --define 'dist suse'
  rpmbuild -ba $spec_file --target i386 --define 'dist suse'
  rpmbuild -ba $spec_file --target x86_64 --define 'dist redhat'
  rpmbuild -ba $spec_file --target i386 --define 'dist redhat'
done

echo 
echo "!!! RPM Package built !!!"
echo 
