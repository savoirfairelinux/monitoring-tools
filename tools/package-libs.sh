#!/bin/bash

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

set -e

lib_name=$1

# Colors
red='\e[0;31m'
green='\e[0;32m'
NC='\e[0m' # No Color

# -S builds only the source package, the binary one is done by OpenBuildService
# --ignore-bad-version skips the date check, because the files can be more recent
# than the last debian/changelog entry
BUILD_PACKAGE="dpkg-buildpackage -us -uc -S --source-option=-Zgzip --source-option=--ignore-bad-version"

# create build-are folder
BASEDIR=$(dirname $(readlink -f "$0"))/..
BUILD_AREA=$BASEDIR/build-area

cd $BASEDIR
mkdir -p $BUILD_AREA/libs


function build_package {
    # lib, plugin, pack
    package_type=$1
    # package name
    package=$2

    echo
    echo "============================================================="
    echo "             Prepare ${package}"
    echo "============================================================="

    # We extract the last version from the changelog
    cd $BASEDIR/${package_type}s
    version=$(cat ${package}/debian/changelog  | grep 'urgency=' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
    rm -rf $BUILD_AREA/${package_type}s/${package}
    cp -r ${package} $BUILD_AREA/${package_type}s/${package}
    cd $BUILD_AREA/${package_type}s
    tar -czf ${package}_${version}.orig.tar.gz ${package}/ --exclude=${package}/debian* --exclude=${package}/.git* --exclude=${package}/build*

    cd ${package}
    if $BUILD_PACKAGE > ../build-${package}.report 2>&1
    then
        echo -e "${green}Build OK${NC}"
    else
        echo -e "${red}Build ERROR. Please look here: $BUILD_AREA/${package_type}s/build-${package}.report${NC}"
        cat $BUILD_AREA/${package_type}s/build-${package}.report${NC}
    fi
    cd $BASEDIR
}



# plugin packages
if [ "$lib_name" != "" ]
then
    if [ -d $BASEDIR/libs/$lib_name ]
    then
        build_package lib $lib_name
    else
        echo -e "\n${red}${lib_name} is NOT a lib${NC}"
    fi
else
    cd libs
    for lib in `ls -d */ | tr -d '/'`
    do
        build_package lib $lib
    done
fi
