#!/bin/bash
echo build DEB Package
echo 

dpkgbuild=`which dpkg-buildpackage`
dch=`which dch`

if [ -z $dpkgbuild ]
then
    echo "rpmbuild not found. Please install dpkg-dev"
    exit 1
fi

if [ -z $dch ]
then
    echo "dch not found. Please install devscripts"
    exit 1
fi

echo 
echo "!!! BUILD MAIN PACKAGE !!!"
echo

# Set variables
date=`date +%Y%m%d`
DIR=$( cd "$( dirname "$0" )" && pwd )
changelog_file=./debian/changelog

# Prepare version
function prepare_version {
    message=`git log --format=%s |head -1`
    message=`echo "$message" | sed 's/^\* //1'`
    changelog_file=./debian/changelog
    version=$(head -1 $changelog_file | grep "\($date\)" > /dev/null; echo $?)
    if [ $version == '0' ]
    then
        release=`head -1 $changelog_file | cut -d "(" -f 2 | cut -d "-" -f 2 | cut -d ")" -f 1`
        release=$(( $release + 1 ))
        echo $message
        $dch -m -v $date-$release -D stable "$message"
    else
        $dch -m -v $date-1 -D stable "$message"
    fi
}

#cd $DIR/..
#prepare_version
# Create package
#$dpkgbuild -ai386
#$dpkgbuild -aamd64

echo
echo "!!! BUILD NRPE static package !!!"
echo
cd $DIR/../nrpe
nrpe_source=`find . -name "nrpe-*.tar.gz" |grep -v static`
version=${nrpe_source//.\/nrpe-/}
version=${version//.tar.gz/}
rm -rf nrpe-static-sfl_*
rm -rf nrpe-$version
rm -f *.changes
rm -f *.dsc

tar xzf nrpe-*.tar.gz
patch -p0 < static-sfl.patch
mv nrpe-$version nrpe-static-sfl-$version
cp -r debian nrpe-static-sfl-$version
cp nrpe_local.cfg nrpe-static-sfl-$version
cp nrpe.cfg nrpe-static-sfl-$version/nrpe.cfg_sfl
cd nrpe-static-sfl-$version
$dpkgbuild -ai386
cd ..
cp nrpe.cfg nrpe_local.cfg nrpe-static-sfl-$version
cd nrpe-static-sfl-$version
$dpkgbuild -aamd64
cd ..
mv *.deb $DIR/../packages
rm -rf nrpe-static-sfl-$version

echo
echo "!!! BUILD library packages !!!"
echo

cd $DIR/../libs/
for lib in `ls -l | egrep '^d' | awk '{print $NF}'`
do
  echo
  echo "!!!! BUILD $lib lib package !!!!"
  echo
  cd $DIR/../libs/$lib
  prepare_version
  $dpkgbuild -ai386
  $dpkgbuild -aamd64 
done

echo
echo "!!! BUILD plugins packages !!!"
echo

cd $DIR/../shinken-plugins-sfl/
for plugin in `ls -l | egrep '^d' | awk '{print $NF}'`
do
  echo
  echo "!!!! BUILD $plugin plugin package !!!!"
  echo
  cd $DIR/../shinken-plugins-sfl/$plugin
  prepare_version
  $dpkgbuild -ai386
  $dpkgbuild -aamd64 
done



echo 
echo "!!! DEB Packages built !!!"
echo 
