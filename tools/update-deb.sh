#!/bin/bash

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

set -e

package_name=$1

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
mkdir -p $BUILD_AREA/plugins
mkdir -p $BUILD_AREA/packs


function build_package {
    # lib, plugin, pack
    package_type=$1
    # package name
    package=$2

    echo
    echo "============================================================="
    echo "             Prepare $package"
    echo "============================================================="

    # We extract the last version from the changelog
    cd $BASEDIR/${package_type}s
    version=$(cat ${package}/debian/changelog  | grep 'urgency=' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
    rm -rf $BUILD_AREA/${package_type}s/${package}
    cp -r ${package} $BUILD_AREA/${package_type}s
    cd $BUILD_AREA/${package_type}s
    tar -czf ${package}_${version}.orig.tar.gz ${package}/ --exclude=${package}/debian* --exclude=${package}/.git*

    cd ${package}
    $BUILD_PACKAGE > ../build-${package}.report 2>&1
    if [[ $? -eq 0 ]]
    then
        echo -e "${green}Build OK${NC}"
    else
        echo -e "${red}Build ERROR. Please look here: $BUILD_AREA/${package_type}s/build-${package}.report${NC}"
        cat $BUILD_AREA/${package_type}s/build-${package}.report${NC}
    fi
    cd $BASEDIR
}




# libs packages
if [ "$package_name" != "" ]
then
    if [ -d $BASEDIR/libs/$package_name ]
    then
        build_package lib $package_name
    else
        echo -e "\n${red}${package_name} is NOT a lib${NC}"
    fi
else
    cd libs
    for lib in `ls -d */ | tr -d '/'`
    do
        build_package lib $lib
    done
fi

# plugin packages
if [ "$package_name" != "" ]
then
    if [ -d $BASEDIR/plugins/$package_name ]
    then
        build_package plugin $package_name
    else
        echo -e "\n${red}${package_name} is NOT a plugin${NC}"
    fi
else
    cd plugins
    for plugin in `ls -d */ | tr -d '/'`
    do
        build_package plugin $plugin
    done
fi

# pack packages
if [ "$package_name" != "" ]
then
    if [ -d $BASEDIR/packs/$package_name ]
    then
        build_package pack $package_name
    else
        echo -e "\n${red}${package_name} is NOT a pack${NC}"
    fi
else
    cd packs
    for pack in `ls -d */ | tr -d '/'`
    do
        build_package pack $pack
    done
fi

exit 0
