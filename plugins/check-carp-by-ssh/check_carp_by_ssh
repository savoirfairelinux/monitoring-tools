#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check carp status on Soekris using ssh
"""
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
#               check_carp_by_ssh Check carp status on Soekris using ssh
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
import os
from subprocess import Popen, PIPE, STDOUT
import re

PLUGIN_NAME = "check_carp_by_ssh"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4


def print_version():
    """Show plugin version
    """
    version_msg = """
%s.py v%s (sfl-shinken-plugins)

The SFL Shinken Plugins come with ABSOLUTELY NO WARRANTY. You may redistribute
copies of the plugins under the terms of the GNU General Public License.
For more information about these matters, see the file named COPYING.
""" % (PLUGIN_NAME, PLUGIN_VERSION)
    print version_msg


def print_support():
    """Show plugin support
    """
    support_msg = """
Send email to thibault.cohen@savoirfairelinux.com if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to thibault.cohen@savoirfairelinux.com
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
"""
    print support_msg


def print_usage():
    """Show how to use this plugin
    """
    usage_msg = """
%s.py -c <carp-ip> -1 <cross-ip-1> -2 <cross-ip-2>

You must create a user shinken/nagios on each carp hosts
And create ssh key and share it and add ssh pub key of 
the shinken server in each carp hosts...
 
Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -c, --carp-ip=ADDRESS
    Carp IP (IP shared by hosts)
 -1, --cross-ip-1=DOUBLE
    Cross IP owned by the first host
 -2, --cross-ip-2=DOUBLE
    Cross IP owned by the other host

""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    results = {'BACKUP': {},
               'MASTER': {},
               'UNKNOWN': {},
                }
    for cross_ip in (args['cross_ip_1'], args['cross_ip_2']):
        if not args['in_test']:
            process = Popen("ssh -o ConnectTimeout=5 "
                                   + args['carp_ip'] +
                                   " ssh -o ConnectTimeout=5 "
                                   + cross_ip +
                                   " 'ifconfig'",
                                   shell=True,
                                   stdout=PIPE,
                                   stderr=STDOUT)
            output, stderr = process.communicate()
            status = process.poll()
        else:
            # In test
            foutput = open(os.path.join(os.getcwd(), cross_ip + ".txt"))
            output = foutput.read()
            status = 0

        if status != 0:
            print "Fetch data error - %s" % output
            sys.exit(STATE_UNKNOWN)

        carp_name = ''
        for line in output.splitlines():
            if line.startswith('carp'):
                carp_name = line.split(": ")[0]
                result = {}
            elif line.startswith("\t") and carp_name:
                if line.startswith("\tdescription: "):
                    desc = line.split("\tdescription: ")[-1]
                    result['description'] = desc
                if line.startswith("\tcarp: "):
                    status = line.split("\tcarp: ")[-1]
                    if re.match('BACKUP', status):
                        result['status'] = 'BACKUP'
                        results['BACKUP']["__".join((cross_ip, carp_name))] = result
                    elif re.match('MASTER', status):
                        result['status'] = 'MASTER'
                        results['MASTER']["__".join((cross_ip, carp_name))] = result
                    else:
                        result['status'] = 'UNKNOWN'
                        results['UNKNOWN']["__".join((cross_ip, carp_name))] = result

    # Verifications
    ## Check number of carp interfaces in UNKNOWN state
    if len(results['UNKNOWN']) > 0:
        unknown_ints = results['UNKNOWN'].keys()
        print "CARP ERROR - Plugin can get status of interfaces: %s " % ", ".join(unknown_ints)
        sys.exit(STATE_CRITICAL)

    ## Check number of carp interfaces
    if len(results['BACKUP']) != len(results['MASTER']):
        print "CARP ERROR - Bad number of carp interfaces"
        sys.exit(STATE_CRITICAL)

    ## Check if all BACKUP interfaces are on the same host
    backup_ips = list(set([x.split("__")[0] for x in results['BACKUP'].keys()]))
    master_ips = list(set([x.split("__")[0] for x in results['MASTER'].keys()]))
    if len(master_ips) > 1:
        print "CARP ERROR - Interfaces in MASTER state are on the two hosts"
        sys.exit(STATE_CRITICAL)
    if len(backup_ips) > 1:
        print "CARP ERROR - Interfaces in BACKUP state are on the two hosts"
        sys.exit(STATE_CRITICAL)
    else:
        backup_ip = backup_ips[0]
        master_ip = master_ips[0] 

    # All look good !
    msg = "CARP OK - Master cross ip: %s - " % (master_ip)
    msg = msg + "Backup cross ip: %s - " % backup_ip
    msg = msg + "%s interfaces up" % len(results['BACKUP'])
    print msg
    sys.exit(STATE_OK)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['cross_ip_1',
                           'cross_ip_2',
                           'carp_ip']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument `%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'hostname' in args.keys():
        args['hostname'] = '127.0.0.1'


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'hV1:2:c:',
                        ['cross-ip-1', 'cross-ip-2', 'carp-ip',
                         'help', 'version'])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)


    args = {'in_test': False}
    # Detect if nosetests if running
    if sys.argv[0].endswith('nosetests'):
        args['in_test'] = True

    for option_name, value in options:
        if option_name in ("-c", "--carp-ip"):
            args['carp_ip'] = value
        elif option_name in ("-1", "--cross-ip-1"):
            args['cross_ip_1'] = value
        elif option_name in ("-2", "--cross-ip-2"):
            args['cross_ip_2'] = value
        elif option_name in ("-h", "--help"):
            print_version()
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)
        elif option_name in ("-V", "--version"):
            print_version()
            print_support()
            sys.exit(STATE_UNKNOWN)

    check_arguments(args)

    get_data(args)


if __name__ == "__main__":
    main()
