#!/bin/bash
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
#            create_new_plugin.sh Create new shinken plugin from template
#
#
#  Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#

which virtualenv >/dev/null 2>/dev/null
[ $? != 0 ] && echo "virtualenv not installed" && exit -1


which dch >/dev/null 2>/dev/null
[ $? != 0 ] && dch="echo Skipping dch command line : dch" || dch=`which dch`


# Go to git root tree
DIR=$( cd "$( dirname "$0" )" && pwd )
cd $DIR/..


first_name=""
last_name=""
email=""
plugin_type=""
plugin_name=""
plugin_description=""
ready="Y"
date=`date +%Y%m%d`
longdate=`LANG="en" date "+%a %b %d %Y"`

PARSED_OPTIONS=$(getopt -n "$0"  -o f:l:e:t:n:d: --long \
"first_name:,last_name:,email:,plugin_type:plugin_name:plugin_description:"  -- "$@")i

#Bad arguments
if [ $? -ne 0 ];
then
  exit 1
fi

eval set -- "$PARSED_OPTIONS"

while true; 
do
  case "$1" in

    -f|--first_name)
      if [ -n "$2" ];
      then
        first_name=$2
      fi
      shift 2;;

    -l|--last_name)
      if [ -n "$2" ];
      then
        last_name=$2
      fi
      shift 2;;

    -e|--email)
      if [ -n "$2" ];
      then
        email=$2
      fi
      shift 2;;

     -t|--plugin_type)
      if [ -n "$2" ];
      then
        plugin_type=$2
      fi
      shift 2;;

    -n|--plugin_name)
      if [ -n "$2" ];
      then
        plugin_name=$2
      fi
      shift 2;;

     -d|--plugin_description)
      if [ -n "$2" ];
      then
        plugin_description=$2
      fi
      shift 2;;
 
    --|*)
      shift
      break;;

  esac
done

while [ "$first_name" = "" ]
do
 echo "Type your first name:"
 read first_name
done

while [ "$last_name" = "" ]
do
 echo ""
 echo "Type your last name:"
 read last_name
done

while [ "$email" = "" ]
do
  echo ""
  echo "Type your email:"
  read email
done

#eval echo "The part is \$part$n."

while [ "$plugin_type" != "python" ] &&
      [ "$plugin_type" != "shell" ] &&
      [ "$plugin_type" != "perl" ] &&
      [ "$plugin_type" != "c" ] &&
      [ "$plugin_type" != "java" ] &&
      [ "$plugin_type" != "php" ] 
do
  echo ""
  echo "What kind of plugin do you want to create:"
  echo "python, shell, perl?"
  read plugin_type
done

# TODO check if this plugin already exist
while [ "$plugin_name" = "" ]
do
  echo ""
  echo "Type the name of your plugin ( ie: check_ldap ):"
  read plugin_name
done

while [ "$plugin_description" = "" ]
do
  echo ""
  echo "Type a description for you plugin:"
  read plugin_description
done

echo ""
echo ""
echo "I will create a new plugin !"
echo Author: "$first_name $last_name <$email>"
echo Plugin name : $plugin_name
echo Plugin description: $plugin_description
echo ""
echo "Are you OK with this [y/N] ?"
read ready

if [ "$ready" != "Y" ] && [ "$ready" != "y" ]
then
  echo
  echo "Bye !!!"
  exit 1
fi

if [ -e ./shinken-plugins-sfl/$plugin_name ]
then
  echo
  echo "The plugin \`$plugin_name' exists !!!"
  echo
  exit 1
fi

# Create a new folder from template folder
git clone git@projects.savoirfairelinux.com:sfl-shinken-plugins--$plugin_name.git shinken-plugins-sfl/$plugin_name
if [ $? -ne 0 ]
then
    echo "sfl-shinken-plugins--$plugin_name repository doesn't exist"
    echo "Please create it in redmine"
    exit 1
fi

cp -r tools/templates/check_template_$plugin_type/* ./shinken-plugins-sfl/$plugin_name/
cp -r tools/templates/packaging/deb/debian ./shinken-plugins-sfl/$plugin_name/
cp -r tools/templates/gitignore ./shinken-plugins-sfl/$plugin_name/.gitignore
cp -r tools/templates/general/* ./shinken-plugins-sfl/$plugin_name/
cp tools/templates/packaging/rpm/check_template.spec ./shinken-plugins-sfl/$plugin_name/$plugin_name.spec

package_plugin_name=`echo "$plugin_name" |tr "_" "-" `
#### PYTHON ####
if [ "$plugin_type" = "python" ]
then
    mv ./shinken-plugins-sfl/$plugin_name/check_template_$plugin_type.py ./shinken-plugins-sfl/$plugin_name/$plugin_name.py
    chmod +x ./shinken-plugins-sfl/$plugin_name/$plugin_name.py
    mv ./shinken-plugins-sfl/$plugin_name/test/test_check_template_$plugin_type.py  ./shinken-plugins-sfl/$plugin_name/test/test_$plugin_name.py
    # Replace values in template
    cd ./shinken-plugins-sfl/$plugin_name
    $dch --package $package_plugin_name -M --create -D stable -v $date-1 "First commit"
    for f in `find . -type f`
    do
        echo "Prepare file: $f"
        sed -i "s/check_template_$plugin_type.py/$plugin_name.py/g" $f
        sed -i "s/<author_name>/$first_name $last_name/g" $f
        sed -i "s/<author_email>/$email/g" $f
        sed -i "s/<description>/$plugin_description/g" $f
        sed -i "s/<filename>/$plugin_name/g" $f
        sed -i "s/<date>/$date/g" $f
        sed -i "s/<longdate>/$longdate/g" $f
        sed -i "s/check_template_$plugin_type/$plugin_name/g" $f
        sed -i "s/check-template/$package_plugin_name/g" $f
        sed -i "s/check_template/$plugin_name/g" $f
    done
    echo "$plugin_name.py /usr/lib/shinken/plugins/" > debian/$package_plugin_name.install

    sed -i "s|<install>|%{__cp} -pr $plugin_name.py %{buildroot}/%{_libdir}/shinken/plugins/$plugin_name.py|" $plugin_name.spec
    sed -i "s|<files>|%{_libdir}/shinken/plugins/$plugin_name.py|" $plugin_name.spec

    # Set env
    virtualenv --no-site-packages env
    . env/bin/activate
    pip install pep8
    pip install coverage
fi
#### PERL ####
if [ "$plugin_type" = "perl" ]
then
    mv ./shinken-plugins-sfl/$plugin_name/check_template_$plugin_type.pl ./shinken-plugins-sfl/$plugin_name/$plugin_name.pl
    mv ./shinken-plugins-sfl/$plugin_name/check_template_$plugin_type.pm ./shinken-plugins-sfl/$plugin_name/$plugin_name.pm
    mv ./shinken-plugins-sfl/$plugin_name/test/check_template_perl.t ./shinken-plugins-sfl/$plugin_name/test/$plugin_name.t
    chmod +x ./shinken-plugins-sfl/$plugin_name/$plugin_name.pl
    # Replace values in template
    cd ./shinken-plugins-sfl/$plugin_name
    $dch --package $package_plugin_name -M --create -D stable -v $date-1 "First commit"
    for f in `find . -type f`
    do
        echo "Prepare file: $f"
        sed -i "s/check_template_$plugin_type.pl/$plugin_name.pl/g" $f
        sed -i "s/check_template_$plugin_type.pm/$plugin_name.pm/g" $f
        sed -i "s/check_template_$plugin_type.t/$plugin_name.t/g" $f
        sed -i "s/<author_name>/$first_name $last_name/g" $f
        sed -i "s/<author_email>/$email/g" $f
        sed -i "s/<description>/$plugin_description/g" $f
        sed -i "s/<filename>/$plugin_name/g" $f
        sed -i "s/<date>/$date/g" $f
        sed -i "s/<longdate>/$longdate/g" $f
        sed -i "s/check_template_$plugin_type/$plugin_name/g" $f
        sed -i "s/check-template/$package_plugin_name/g" $f
        sed -i "s/check_template/$plugin_name/g" $f
    done
    echo "$plugin_name.pl /usr/lib/shinken/plugins/" > debian/$package_plugin_name.install
    echo "$plugin_name.pm /usr/lib/shinken/plugins/" >> debian/$package_plugin_name.install

    sed -i "s|<install>|%{__cp} -pr $plugin_name.pl %{buildroot}/%{_libdir}/shinken/plugins/$plugin_name.pl\n%{__cp} -pr $plugin_name.pm %{buildroot}/%{_libdir}/shinken/plugins/$plugin_name.pm|" $plugin_name.spec
    sed -i "s|<files>|%{_libdir}/shinken/plugins/$plugin_name.pl\n%{_libdir}/shinken/plugins/$plugin_name.pm|" $plugin_name.spec
fi
#### BASH ####
if [ "$plugin_type" = "shell" ]
then
    mv ./shinken-plugins-sfl/$plugin_name/check_template_$plugin_type.sh ./shinken-plugins-sfl/$plugin_name/$plugin_name.sh
    mv ./shinken-plugins-sfl/$plugin_name/check_template_$plugin_type.inc ./shinken-plugins-sfl/$plugin_name/$plugin_name.inc
    mv ./shinken-plugins-sfl/$plugin_name/test/test_check_template_shell.sh ./shinken-plugins-sfl/$plugin_name/test/test_$plugin_name.sh
    chmod +x ./shinken-plugins-sfl/$plugin_name/$plugin_name.sh
    # Replace values in template
    cd ./shinken-plugins-sfl/$plugin_name
    $dch --package $package_plugin_name -M --create -D stable -v $date-1 "First commit"
    for f in `find . -type f`
    do
        echo "Prepare file: $f"
        sed -i "s/check_template_$plugin_type.sh/$plugin_name.sh/g" $f
        sed -i "s/check_template_$plugin_type.inc/$plugin_name.inc/g" $f
        sed -i "s/<author_name>/$first_name $last_name/g" $f
        sed -i "s/<author_email>/$email/g" $f
        sed -i "s/<description>/$plugin_description/g" $f
        sed -i "s/<filename>/$plugin_name/g" $f
        sed -i "s/<date>/$date/g" $f
        sed -i "s/<longdate>/$longdate/g" $f
        sed -i "s/check_template_$plugin_type/$plugin_name/g" $f
        sed -i "s/check-template/$package_plugin_name/g" $f
        sed -i "s/check_template/$plugin_name/g" $f
    done
    echo "$plugin_name.sh /usr/lib/shinken/plugins/" > debian/$package_plugin_name.install
    echo "$plugin_name.inc /usr/lib/shinken/plugins/" >> debian/$package_plugin_name.install

    sed -i "s|<install>|%{__cp} -pr $plugin_name.inc %{buildroot}/%{_libdir}/shinken/plugins/$plugin_name.inc\n%{__cp} -pr $plugin_name.sh %{buildroot}/%{_libdir}/shinken/plugins/$plugin_name.sh|" $plugin_name.spec
    sed -i "s|<files>|%{_libdir}/shinken/plugins/$plugin_name.inc\n%{_libdir}/shinken/plugins/$plugin_name.sh|" $plugin_name.spec
fi

# We are into the plugin dir
git add .
git commit -m "First commit for $plugin_name"
git push origin master

cd ../../
# We are now at top level
git submodule add git@projects.savoirfairelinux.com:sfl-shinken-plugins--$plugin_name.git shinken-plugins-sfl/$plugin_name 2>&1
git commit -m "Adding $plugin_name to repo"
git push origin master


echo "============================================="
echo "           Your plugin is ready !!!          "
