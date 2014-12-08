#!/bin/sh
# -*- coding: utf-8 -*-
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
#               check_cpu.inc Plugin to check CPU usage
#
#
#     Author: 2009, Mike Adolphs (http://www.matejunkie.com/)
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#


#############################################
#                                           #
#    Variables                              #
#                                           #
#############################################
PROGNAME=`basename $0`
PROGPATH=`echo $0 | sed -e 's,[\\/][^\\/][^\\/]*$,,'`
REVISION="1.1"

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
    echo ""
    support
    exit $STATE_UNKNOWN
}

#############################################
#                                           #
#    Print Usage                            #
#    MUST BE REWRITTEN                      #
#                                           #
#############################################

print_usage(){
    echo ""
    echo "$PROGNAME is a Shinken/Nagios plugin to monitor CPU utilization. It makes"
    echo "use of /proc/stat and calculates it through Jiffies rather than"
    echo "using another frontend tool like iostat or top."
    echo "When using optional warning/critical thresholds all values except"
    echo "idle and nice are aggregated and compared to the thresholds."
    echo "You can change it with -v option".
    echo ""
    echo "$PROGNAME [-v <values>] [-i <interval>] [-w <threshold>] [-c <threshold>]"
    echo ""
    echo "Options:"
    echo "  -v)"
    echo "    Define the sum of values use for thresholds"
    echo "    e.g. : -a oqfs"
    echo "    default : usoqf"
    echo "    u => user"
    echo "    n => nice"
    echo "    s => sys"
    echo "    o => iowait"
    echo "    q => irq"
    echo "    f => softirq"
    echo "    i => idle"
    echo "  -i)"
    echo "    Defines the pause between the two times /proc/stat is being"
    echo "    parsed. Higher values could lead to more accurate result."
    echo "    Default is: 1 second"
    echo "  -w)"
    echo "    Sets a warning level for CPU user. Default is: off"
    echo "  -c)"
    echo "    Sets a critical level for CPU user. Default is: off"
}

#############################################
#                                           #
#    Check arguments validity               #
#    MUST BE REWRITTEN                      #
#                                           #
#############################################

check_arguments(){
    if [ -z "$alert" ]
    then
        alert="usoqf"
    fi
    if [ -z "$interval" ]
    then
        interval=1
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
val_wcdiff() {
    if [ ${warning} -gt ${critical} ]
    then
        wcdiff=1
    fi
}

get_cpuvals() {
    tmp1_cpu_user=`grep -m1 '^cpu' /proc/stat|awk '{print $2}'`
    tmp1_cpu_nice=`grep -m1 '^cpu' /proc/stat|awk '{print $3}'`
    tmp1_cpu_sys=`grep -m1 '^cpu' /proc/stat|awk '{print $4}'`
    tmp1_cpu_idle=`grep -m1 '^cpu' /proc/stat|awk '{print $5}'`
    tmp1_cpu_iowait=`grep -m1 '^cpu' /proc/stat|awk '{print $6}'`
    tmp1_cpu_irq=`grep -m1 '^cpu' /proc/stat|awk '{print $7}'`
    tmp1_cpu_softirq=`grep -m1 '^cpu' /proc/stat|awk '{print $8}'`
    tmp1_cpu_total=`expr $tmp1_cpu_user + $tmp1_cpu_nice + $tmp1_cpu_sys + $tmp1_cpu_idle + $tmp1_cpu_iowait + $tmp1_cpu_irq + $tmp1_cpu_softirq`

    sleep $interval

    tmp2_cpu_user=`grep -m1 '^cpu' /proc/stat|awk '{print $2}'`
    tmp2_cpu_nice=`grep -m1 '^cpu' /proc/stat|awk '{print $3}'`
    tmp2_cpu_sys=`grep -m1 '^cpu' /proc/stat|awk '{print $4}'`
    tmp2_cpu_idle=`grep -m1 '^cpu' /proc/stat|awk '{print $5}'`
    tmp2_cpu_iowait=`grep -m1 '^cpu' /proc/stat|awk '{print $6}'`
    tmp2_cpu_irq=`grep -m1 '^cpu' /proc/stat|awk '{print $7}'`
    tmp2_cpu_softirq=`grep -m1 '^cpu' /proc/stat|awk '{print $8}'`
    tmp2_cpu_total=`expr $tmp2_cpu_user + $tmp2_cpu_nice + $tmp2_cpu_sys + $tmp2_cpu_idle + $tmp2_cpu_iowait + $tmp2_cpu_irq + $tmp2_cpu_softirq`

    diff_cpu_user=`echo "${tmp2_cpu_user} - ${tmp1_cpu_user}" | bc -l`
    diff_cpu_nice=`echo "${tmp2_cpu_nice} - ${tmp1_cpu_nice}" | bc -l`
    diff_cpu_sys=`echo "${tmp2_cpu_sys} - ${tmp1_cpu_sys}" | bc -l`
    diff_cpu_idle=`echo "${tmp2_cpu_idle} - ${tmp1_cpu_idle}" | bc -l`
    diff_cpu_iowait=`echo "${tmp2_cpu_iowait} - ${tmp1_cpu_iowait}" | bc -l`
    diff_cpu_irq=`echo "${tmp2_cpu_irq} - ${tmp1_cpu_irq}" | bc -l`
    diff_cpu_softirq=`echo "${tmp2_cpu_softirq} - ${tmp1_cpu_softirq}"  | bc -l`
    diff_cpu_total=`echo "${tmp2_cpu_total} - ${tmp1_cpu_total}" | bc -l`

    cpu_user=`echo "scale=2; (1000*${diff_cpu_user}/${diff_cpu_total}+5)/10" | bc -l | sed 's/^\./0./'`
    cpu_nice=`echo "scale=2; (1000*${diff_cpu_nice}/${diff_cpu_total}+5)/10" | bc -l | sed 's/^\./0./'`
    cpu_sys=`echo "scale=2; (1000*${diff_cpu_sys}/${diff_cpu_total}+5)/10" | bc -l | sed 's/^\./0./'`
    cpu_idle=`echo "scale=2; (1000*${diff_cpu_idle}/${diff_cpu_total}+5)/10" | bc -l | sed 's/^\./0./'`
    cpu_iowait=`echo "scale=2; (1000*${diff_cpu_iowait}/${diff_cpu_total}+5) /10" | bc -l | sed 's/^\./0./'`
    cpu_irq=`echo "scale=2; (1000*${diff_cpu_irq}/${diff_cpu_total}+5)/10" | bc -l | sed 's/^\./0./'`
    cpu_softirq=`echo "scale=2; (1000*${diff_cpu_softirq}/${diff_cpu_total} +5)/10" | bc -l | sed 's/^\./0./'`
    cpu_total=`echo "scale=2; (1000*${diff_cpu_total}/${diff_cpu_total}+5) /10" | bc -l | sed 's/^\./0./'`
    get_cpu_usage
}

get_cpu_usage() {
    total="0" 
    if [ `echo ${alert} | grep u` ]
    then
        total="${total}+${cpu_user}"
    fi
    if [ `echo ${alert} | grep n` ]
    then
        total="${total}+${cpu_nice}"
    fi
    if [ `echo ${alert} | grep s` ]
    then
        total="${total}+${cpu_sys}"
    fi
    if [ `echo ${alert} | grep o` ]
    then
        total="${total}+${cpu_iowait}"
    fi
    if [ `echo ${alert} | grep q` ]
    then
        total="${total}+${cpu_irq}"
    fi
    if [ `echo ${alert} | grep f` ]
    then
        total="${total}+${cpu_softirq}"
    fi
    if [ `echo ${alert} | grep i` ]
    then
        total="${total}+${cpu_idle}"
    fi
    cpu_usage=`echo "($total)/1" | bc`
}

do_output() {
    output="user: ${cpu_user}, nice: ${cpu_nice}, sys: ${cpu_sys}, iowait: ${cpu_iowait}, irq: ${cpu_irq}, softirq: ${cpu_softirq} idle: ${cpu_idle}"
    output="$output , cpu_usage_$alert:$cpu_usage"
}

do_perfdata() {
    perfdata="'user'=${cpu_user};;;0;100 'nice'=${cpu_nice};;0;100 'sys'=${cpu_sys};;;0;100 'softirq'=${cpu_softirq};;;0;100 'iowait'=${cpu_iowait};;;0;100 'irq'=${cpu_irq};;;0;100 'idle'=${cpu_idle};;;0;100"
    if [ -n "$warning" -a -n "$critical" ]
    then
        perfdata="$perfdata cpu_usage_$alert=$cpu_usage;$warning;$critical;0;100"
    else
        perfdata="$perfdata cpu_usage_$alert=$cpu_usage;;;0;100"
    fi
}


get_data(){
    if [ -n "$warning" -a -n "$critical" ]
    then
        val_wcdiff
        if [ "$wcdiff" = 1 ]
        then
            echo "Please adjust your warning/critical thresholds. The warning must be lower than the critical level!"
            exit $STATE_UNKNOWN
        fi
    fi

    get_cpuvals
    do_output
    do_perfdata

    if [ -n "$warning" -a -n "$critical" ]
    then
        if [ "$cpu_usage" -ge "$warning" -a "$cpu_usage" -lt "$critical" ]
        then
            echo "WARNING - ${output} | ${perfdata}"
            exit $STATE_WARNING
        elif [ "$cpu_usage" -ge "$critical" ]
        then
            echo "CRITICAL - ${output} | ${perfdata}"
            exit $STATE_CRITICAL
        else
            echo "OK - ${output} | ${perfdata}"
            exit $STATE_OK
        fi
    else
        echo "OK - ${output} | ${perfdata}"
        exit $STATE_OK
    fi
}
