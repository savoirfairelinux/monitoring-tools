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
#               run_tests.sh Plugin to check CPU usage
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#


oneTimeSetUp() {
    echo "--------------------------"
    . ./check_cpu.inc 
    . ./check_cpu_utils.sh
}

tearDown() {
    echo "--------------------------"
}

testCheckcheckbashisms() {
    file=check_cpu.inc
    result=`test/jenkins/checkbashisms -n -f -x ./$file 2>&1`
    assertTrue " CheckBashisms on $file failed : $result" '[ "$result" = "" ]'

    file=check_cpu
    result=`test/jenkins/checkbashisms -n -f -x ./$file 2>&1`
    assertTrue " CheckBashisms on $file failed : $result" '[ "$result" = "" ]'
}


testHelp() {
    result=`print_help`
    t=`echo $result |grep "check_cpu.sh"`
    assertTrue " Test print Usage Failed" '[ ! -z "$t" ]'
}

testDefaultArgs() {
    alert="usoqf"
    interval=1
    result=`get_data`
    t=`echo $result |grep "cpu_usage_usoqf"`
    assertTrue " Test Alert option default value failed" '[ ! -z "$t" ]'
}

testArgs() {
    alert="nusoqf"
    interval=2
    warning=80
    critical=90
    result=`get_data`
    t=`echo $result |grep "cpu_usage_nusoqf"`
    assertTrue " Test Alert option default value failed" '[ ! -z "$t" ]'
}


testBadThresholds() {
    alert="nusoqf"
    interval=2
    warning=95
    critical=90
    result=`get_data`
    t=`echo $result |grep "Please adjust your warning/critical"`
    assertTrue " Test Alert option default value failed" '[ ! -z "$t" ]'
}

. ./test/jenkins/shunit2/shunit2
