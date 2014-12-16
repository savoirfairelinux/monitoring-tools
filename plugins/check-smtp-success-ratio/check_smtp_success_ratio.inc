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
#               check_smtp_success_ratio.inc Given a maillog, 
#               checks for a good ratio of sent versus total emails.
#
#
#     Author: Stéphane Duchesneau <stephane.duchesneau@savoirfairelinux.com> 
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
#                                           #
#############################################

print_usage(){
    echo "Usage:"
    echo "$PROGNAME"
    echo ""
    echo "This plugin checks for a success ratio in emails logs"
    echo ""
    echo " -w {warning}"
    echo "    Threshold for a warning in % [DEFAULT: 5]"
    echo " -c {critical}"
    echo "    Threshold for a critical in % [DEFAULT: 101 (never fire critical alert)]"
    echo " -f {filename}"
    echo "    Select file to use as source for mail log [DEFAULT: /var/log/mail.log]" 
    echo " -F {filename2}"
    echo "    Select file fall back to if primary file is too short [DEFAULT: /var/log/mail.log.1]"
    echo " -l {lines}"
    echo "    Number of lines to read from at the end of the file [DEFAULT: 1000]"
    echo " -h, --help"
    echo "    Print detailed help screen"
    echo " -V, --version"
    echo "    Print version information"
    echo ""
}

#############################################
#                                           #
#    Check arguments validity               #
#                                           #
#############################################

check_arguments(){
    if [ -z "$warning" ]
    then
        warning=5
    fi
    if [ -z "$critical" ]
    then
        critical=101
    fi
    if [ -z "$filename" ]
    then
        filename="/var/log/mail.log"
    fi
    if [ -z "$filename2" ]
    then
        filename2="/var/log/mail.log.1"
    fi
    if [ -z "$lines" ]
    then
        lines=1000
    fi
}

#############################################
#                                           #
#    Get data and prepare output            #
#    testdata variable have to have one     #
#     of this word inside :                 #
#      - WARNING                            #
#      - CRITICAL                           #
#      - OK                                 #
#                                           #
#############################################
get_data(){
    TMPFILE=`mktemp`
    TMPFILE2=`mktemp`

    tac $filename |grep status= |egrep '(yahoo.com|yahoo.co.jp|hotmail.com|gmail.com|yahoo.fr|yahoo.ca|msn.ca|msn.com|live.com|live.ca|orange.fr|orange.com|hotmail.fr|free.fr|wanadoo.fr|voila.fr|sympatico.ca|videotron.com|videotron.ca|sfr.fr)' |head -n $lines > $TMPFILE 2>/dev/null
    file1lc=`cat $TMPFILE | wc -l`

    if [ "$file1lc" -lt "$lines" ]
    then
        echo "adding"
        morelines=`echo $lines - $file1lc | bc`
        tac $filename2 |grep status= |egrep '(yahoo.com|hotmail.com|gmail.com|yahoo.fr|yahoo.ca|msn.ca|msn.com|live.com|live.ca|orange.fr|orange.com|hotmail.fr|free.fr|wanadoo.fr|voila.fr|sympatico.ca|videotron.com|videotron.ca|sfr.fr)' |head -n $morelines >> $TMPFILE
    fi

    awk '!x[$7]++' $TMPFILE > $TMPFILE2
    
    NBEMAILS=`grep status= $TMPFILE2 |wc -l`
    NBSENT=`grep status=sent $TMPFILE2|wc -l`
    NBREFUSED=`grep refused.to.talk $TMPFILE2|wc -l`
    rm -f $TMPFILE 
    
    # prevent DIV/0
    if [ $NBEMAILS = 0 ]; then 
        REFUSALRATIO=0
    else
        REFUSALRATIO=`echo $NBREFUSED \* 100 / $NBEMAILS | bc`
    fi

    echo $critical $warning
    if [ $REFUSALRATIO -gt $critical ]; then
        testdata="CRITICAL - Email failure ratio too high |totalemails=$NBEMAILS;;;0 successemails=$NBSENT;;;0 refusedemails=$NBREFUSED;;;0 refusalratio=$REFUSALRATIO%;$warning;$critical;0;100"
        status=2
    elif [ $REFUSALRATIO -gt $warning ]; then
        testdata="WARNING - Email failure ratio too high |totalemails=$NBEMAILS;;;0 successemails=$NBSENT;;;0 refusedemails=$NBREFUSED;;;0 refusalratio=$REFUSALRATIO%;$warning;$critical;0;100"
        status=1
    else
        testdata="OK - Email failure ratio acceptable |totalemails=$NBEMAILS;;;0 successemails=$NBSENT;;;0 refusedemails=$NBREFUSED;;;0 refusalratio=$REFUSALRATIO%;$warning;$critical;0;100"
        status=0
    fi
}
