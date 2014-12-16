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
#               check_asterisk_cdr_status.inc Check asterisk sql cdr
#
#
#     Author: Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com> 
#


#############################################
#                                           #
#    Variables                              #
#                                           #
#############################################
PROGNAME=`basename $0`
PROGPATH=`echo $0 | sed -e 's,[\\/][^\\/][^\\/]*$,,'`
REVISION="0.1"


#############################################
#                                           #
#    Print Help                             #
#                                           #
#############################################
print_help(){
    print_revision $PROGNAME $REVISION
    echo ""
    print_usage
    echo ""
    support
    exit 0
}

#############################################
#                                           #
#    Print Usage                            #
#    MUST BE REWRITTEN                      #
#                                           #
#############################################

print_usage(){
    echo "Usage:"
    echo "$PROGNAME"
    echo ""
    echo "This plugin is a template written in shell script"
    echo ""
    echo " -h, --help"
    echo "    Print detailed help screen"
    echo " -V, --version"
    echo "    Print version information"
    echo ""
}

#############################################
#                                           #
#    Check arguments validity               #
#    MUST BE REWRITTEN                      #
#                                           #
#############################################

check_arguments(){
    if [ -z "$warning" ]
    then
        echo "Warning option is missing" >&2
        print_help
        exit 3
    fi
    if [ -z "$critical" ]
    then
        echo "Critical option is missing" >&2
        print_help
        exit 3
    fi
}

#############################################
#                                           #
#    Get data and prepare output            #
#    MUST BE REWRITTEN                      #
#    testdata variable have to have one     #
#     of this word inside :                 #
#      - WARNING                            #
#      - CRITICAL                           #
#      - OK                                 #
#                                           #
#############################################
get_data(){
    status=1
    data=`date "+%M"`
    if [ $(( $data % 2 )) -eq 0 ]
    then
        testdata="WARNING - time : `date "+%H:%M"` |minute=$data;0;60;"

    elif [ $(( $data % 3 )) -eq 0 ]
    then
        testdata="CRITICAL - time : `date "+%H:%M"` |minute=$data;0;60;"
    else
        testdata="OK - time : `date "+%H:%M"` | minute=$data;0;60;"
    fi
    status=0
}
