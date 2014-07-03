#!/bin/sh
#
#
#     Copyright (C) 2012 Savoir-Faire Linux Inc. 
#
#     This program is free software; you can redistribute it and/or modify 
#     it under the terms of the GNU General Public License as published by 
#     the Free Software Foundation; either version 3 of the License, or 
#     (at your option) any later version. 
#
#     This program is distributed in the hope that it will be useful, 
#     but WITHOUT ANY WARRANTY; without even the implied warranty of 
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#     GNU General Public License for more details. 
#
#     You should have received a copy of the GNU General Public License 
#     along with this program; if not, write to the Free Software 
#     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA. 
#
#     Projects :
#               SFL Shinken plugins
#
#     File :
#               check_template_shell.sh <description>
#
#
#     Author: <author_name> <<author_email>> 
#
#

if [ -e $PROGPATH/utils.sh ]
then
    . $PROGPATH/utils.sh
elif [ -e ./utils.sh ]
then
    . ./utils.sh
else
    echo "UNKNOWN : utils.sh not found"
    exit 1
fi

if [ -e $PROGPATH/check_template_shell.inc ]
then
    . $PROGPATH/check_template_shell.inc
elif [ -e ./check_template_shell.inc ]
then
    . ./check_template_shell.inc
else
    echo "UNKNOWN : check_template_shell.inc not found"
    exit 1
fi

#############################################
#                                           #
#    Return output and exit code            #
#                                           #
#############################################

while getopts "hv:w:c:" opt
do
    case "$opt" in
        w)
            warning=$OPTARG
        ;;
        c)
            critical=$OPTARG
        ;;
        h)
            print_help
            exit 3
        ;;
        v)
            print_revision $PROGNAME $REVISION
            exit 3
        ;;
        \?)
            print_help
            exit 3
        ;;
        :)
            # maybe useless
            echo "Option -$OPTARG requires an argument." >&2
            print_help
        ;;
    esac
done

check_arguments

get_data

if test ${status} -eq 1; then
    echo "UNKNOWN: The plug-in has failed to function"
    exit $STATE_UNKNOWN

elif echo ${testdata} | egrep WARNING > /dev/null; then
    echo "$testdata"
    exit $STATE_WARNING

elif echo ${testdata} | egrep CRITICAL > /dev/null; then
    echo "$testdata"
    exit $STATE_CRITICAL

else test ${status} -eq 0 ;
    echo "$testdata"
    exit $STATE_OK
fi
