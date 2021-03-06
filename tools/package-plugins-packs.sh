#!/bin/bash

# prevents grep from adding line numbers, etc
export GREP_OPTIONS=""

set -e

plugin_name=$1
pack_name=$1

# Colors
red='\e[0;31m'
green='\e[0;32m'
NC='\e[0m' # No Color

# -S builds only the source package, the binary one is done by OpenBuildService
# --ignore-bad-version skips the date check, because the files can be more recent
# than the last debian/changelog entry
BUILD_DEB="dpkg-buildpackage -tc -us -uc --source-option=-Zgzip --source-option=--ignore-bad-version"

# create build-are folder
BASEDIR=$(dirname $(readlink -f "$0"))/..
BUILD_AREA=$BASEDIR/build-area

cd $BASEDIR
mkdir -p $BUILD_AREA/plugins
mkdir -p $BUILD_AREA/packs


function build_package {
    # lib, plugin, pack
    package_type=$1
    # package name
    package=$2
    # prefix
    prefix=monitoring-${package_type}s-sfl

    echo
    echo "============================================================="
    echo "             Prepare ${prefix}-${package}"
    echo "============================================================="

    # We extract the last version from the changelog
    cd $BASEDIR/${package_type}s
    version=$(cat ${package}/debian/changelog  | grep 'urgency=' | head -n 1 | awk '{print $2}' | tr -d '()' | cut -d '-' -f 1)
    rm -rf $BUILD_AREA/${package_type}s/${prefix}-${package}
    cp -r ${package} $BUILD_AREA/${package_type}s/${prefix}-${package}
    cd $BUILD_AREA/${package_type}s
    find ${prefix}-${package} -type f -name "*.pyc" -exec rm -f {} \;
    tar -czf ${prefix}-${package}_${version}.orig.tar.gz ${prefix}-${package}/ --exclude=${prefix}-${package}/debian* --exclude=${prefix}-${package}/.git* --exclude=${prefix}-${package}/build  --exclude=${prefix}-${package}/*.pyc  --exclude=*.pyc 
    cp ${prefix}-${package}/${prefix}-${package}.spec . 2> /dev/null || echo spec file is missing, RPM packages can NOT be done

    if [ -e "${prefix}-${package}.spec" ]
    then
        if rpmbuild -ba ${prefix}-${package}.spec --define "_sourcedir $BUILD_AREA/${package_type}s" > $BUILD_AREA/${package_type}s/build-${prefix}-${package}.rpm.report 2>&1
        then
            echo -e "${green}Build RPM OK${NC}"
        else
            echo -e "${red}Build RPM ERROR. Please look here: $BUILD_AREA/${package_type}s/build-${prefix}-${package}.rpm.report${NC}"
            cat  $BUILD_AREA/${package_type}s/build-${prefix}-${package}.rpm.report
        fi
    fi

    cd ${prefix}-${package}
    if $BUILD_DEB > ../build-${prefix}-${package}.deb.report 2>&1
    then
        echo -e "${green}Build DEB OK${NC}"
    else
        echo -e "${red}Build DEB ERROR. Please look here: $BUILD_AREA/${package_type}s/build-${prefix}-${package}.deb.report${NC}"
        cat $BUILD_AREA/${package_type}s/build-${prefix}-${package}.deb.report
    fi
    cd $BASEDIR
}



# plugin packages
if [ "$plugin_name" != "" ]
then
    if [ -d $BASEDIR/plugins/$plugin_name ]
    then
        build_package plugin $plugin_name
    else
        echo -e "\n${red}${plugin_name} is NOT a plugin${NC}"
    fi
else
    cd plugins
    for plugin in `ls -d */ | tr -d '/'`
    do
        build_package plugin $plugin
    done
fi

# pack packages
if [ "$pack_name" != "" ]
then
    if [ -d $BASEDIR/packs/$pack_name ]
    then
        build_package pack $pack_name
    else
        echo -e "\n${red}${pack_name} is NOT a pack${NC}"
    fi
else
    cd packs
    for pack in `ls -d */ | tr -d '/'`
    do
        build_package pack $pack
    done
fi

exit 0
