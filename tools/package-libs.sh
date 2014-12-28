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
BUILD_DEB="dpkg-buildpackage -tc -us -uc -S --source-option=-Zgzip --source-option=--ignore-bad-version"

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
    find ${package} -type f -name "*.pyc" -exec rm -f {} \;
    tar -czf ${package}_${version}.orig.tar.gz ${package}/ --exclude=${package}/debian* --exclude=${package}/.git* --exclude=${package}/build* --exclude=${prefix}-${package}/build  --exclude=${prefix}-${package}/*.pyc  --exclude=*.pyc
    cp ${package}/${package}.spec . 2> /dev/null || echo spec file is missing, RPM packages can NOT be done

    if [ -e "${package}.spec" ]
    then
        if rpmbuild -ba ${package}.spec --define "_sourcedir $BUILD_AREA/${package_type}s" > $BUILD_AREA/${package_type}s/build-${package}.rpm.report 2>&1
        then
            echo -e "${green}Build RPM OK${NC}"
        else
            echo -e "${red}Build RPM ERROR. Please look here: $BUILD_AREA/${package_type}s/build-${prefix}-${package}.rpm.report${NC}"
            cat  $BUILD_AREA/${package_type}s/build-${prefix}-${package}.rpm.report
        fi
    fi


    cd ${package}
    if $BUILD_DEB > ../build-${package}.deb.report 2>&1
    then
        echo -e "${green}Build DEB OK${NC}"
    else
        echo -e "${red}Build DEB ERROR. Please look here: $BUILD_AREA/${package_type}s/build-${package}.report${NC}"
        cat $BUILD_AREA/${package_type}s/build-${package}.deb.report
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
