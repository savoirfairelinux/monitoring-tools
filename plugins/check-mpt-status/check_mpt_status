#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check mpt HW RAID controllers status
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
#               check_mpt_status Check mpt HW RAID controllers status
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
from subprocess import Popen, PIPE, STDOUT

PLUGIN_NAME = "check_mpt_status"
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
%s.py [-h] [-V]

Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    # Test mode ??
    if not args['in_test']:
        # No test mode
        command = ['mpt-status', '-s']
        process = Popen("mpt-status -s",
                        shell=True,
                        stdout=PIPE,
                        stderr=PIPE)
        output, stderr = process.communicate()
        status = process.poll()

    else:
        # Test mode
        output = """log_id 0 OPTIMAL
phys_id 1 ONLINE
phys_id 0 ONLINE
log_id 1 OPTIMAL
phys_id 1 ONLINE
phys_id 0 ONLINE
phys_id 2 ONLINE
"""
    if not output and status != 0:
        print "UNKNOWN - Error executing mpt-status command - ERROR: '%s'" % stderr.strip()
        exit_code = STATE_UNKNOWN
        sys.exit(exit_code)
    elif not output:
        print "UNKNOWN - Not output (command 'mpt-status -s')"
        exit_code = STATE_UNKNOWN
        sys.exit(exit_code)

    msg = ''
    exit_code = STATE_OK
    for line in output.splitlines():
        if line.startswith("log_id"):
            _, array_id, state = line.split(" ")
            if msg:
                msg = msg + " ) - "
            msg += "Array %s: %s (" % (array_id, state)
            new_array = True
            if state != 'OPTIMAL':
                exit_code = STATE_CRITICAL
        elif line.startswith("phys_id"):
            if new_array == False:
                msg = msg + " -"
            _, disk_id, state = line.split(" ")
            msg = msg + " Disk %s: %s" % (disk_id, state)
            new_array = False
            if state != 'ONLINE' and state != 'ENABLED':
                exit_code = STATE_CRITICAL

    msg = msg + " )"

    if exit_code == STATE_CRITICAL:
        msg = "CRITICAL - " + msg
    else:
        msg = "OK - " + msg
    print msg
    sys.exit(exit_code)


def check_arguments(args):
    """Check mandatory fields
    """

def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'hV',
                        ['help', 'version', ])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {'in_test': False}
    # Detect if nosetests if running
    if sys.argv[0].endswith('nosetests'):
        args['in_test'] = True

    for option_name, value in options:
        if option_name in ("-h", "--help"):
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
