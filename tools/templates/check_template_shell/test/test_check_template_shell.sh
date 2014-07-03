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
#               run_tests.sh <description>
#
#
#     Author: <author_name> <<author_email>>
#


oneTimeSetUp() {
    echo "--------------------------"
    . ./check_template_shell.inc 
}

tearDown() {
    echo "--------------------------"
}

testCheckcheckbashisms() {
    file=check_template_shell.inc
    result=`test/jenkins/checkbashisms -n -f -x ./$file 2>&1`
    assertTrue " CheckBashisms on $file failed : $result" '[ "$result" = "" ]'

    file=check_template_shell.sh
    result=`test/jenkins/checkbashisms -n -f -x ./$file 2>&1`
    assertTrue " CheckBashisms on $file failed : $result" '[ "$result" = "" ]'
}

testUsage() {
    result=`print_usage`
    t=`echo $result |grep "^Usage:"`
    assertTrue " Test print Usage Failed" '[ ! -z "$t" ]'
}


. ./test/jenkins/shunit2/shunit2
