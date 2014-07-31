#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fake plugin for nagios
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
#               check_fake Fake plugin for nagios
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
import random
import os
import string
import time

PLUGIN_NAME = "check_fake"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4

STATES = {0: 'OK',
          1: 'WARNING',
          2: 'CRITICAL',
          3: 'UNKNOWN',
          4: 'DEPENDENT',
          }

POOL_FOLDER = '/tmp/shinken/'


def print_version():
    """Show plugin version
    """
    version_msg = """
%s v%s (sfl-shinken-plugins)

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
%s -H <hostname> -S <servicename> -t <type> [-l <latency>]\
 [-s <state>] [-e <error-state>]

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=HOSTNAME
    Hostname from configuration
 -S, --servicename=SERVICENAME
    Service description from configuration
 -t, --type=TYPE
    Ouput type: INT64, INT32, INT16, TEXT or BOOL
 -l, --latency=SECONDS
    Plugin latency, fake slow plugin ...
    Default: 0
 -s, --state=STATE
    State in normal mode : 0 (OK), 1 (WARNING), 2 (CRITICAL), 3 (UNKNOWN)
    Default: 0
 -e, --error-state=STATE
    State in error mode : 0 (OK), 1 (WARNING), 2 (CRITICAL), 3 (UNKNOWN)
    Default: 2
 -V, --version
    Print version information
""" % PLUGIN_NAME
    print usage_msg


def get_data(kargs):
    """Fetch data
    """
    latency = kargs['latency']
    output_type = kargs['type']

    # Sleep ...
    time.sleep(latency)

    # Prepare output
    perf = ""
    if output_type == 'BOOL':
        value = random.randrange(0, 2)
    elif output_type == 'TEXT':
        raw_text = "".join([chr(random.randrange(0, 256)) for i in xrange(64)])
        value = raw_text.decode('latin9')
    elif output_type == 'INT16':
        value = random.randrange(-32768, 32768)
        perf = " | value=%(value)s;;;-32768;32767"
    elif output_type == 'INT32':
        value = random.randrange(-2147483648, 2147483648)
        perf = " | value=%(value)s;;;-2147483648;2147483647"
    elif output_type == 'INT64':
        value = random.randrange(-9223372036854775808, 9223372036854775808)
        perf = " | value=%(value)s;;;-9223372036854775808;9223372036854775807"

    # Check file existance
    filename = kargs['hostname'] + "_" + kargs['servicename']
    filename = os.path.join(POOL_FOLDER, filename)
    if os.path.exists(filename):
        exit_code = kargs['error-state']
    else:
        exit_code = kargs['state']

    # Set output
    var = {}
    var['state'] = STATES[exit_code]
    var['value'] = value
    output = "%(state)s: %(value)s" + perf
    output = output % var
    print output
    sys.exit(exit_code)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['hostname',
                           'type',
                           'servicename']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument `%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'latency' in args.keys():
        args['latency'] = 0

    if not 'state' in args.keys():
        args['state'] = 0

    if not 'error-state' in args.keys():
        args['error-state'] = 2

    if not args['type'] in ['INT64', 'INT32', 'INT16', 'TEXT', 'BOOL']:
        print "Type must be INT64, INT32, INT16, TEXT or BOOL"
        sys.exit(STATE_UNKNOWN)

    if not args['state'] in STATES:
        print "State must be 0, 1, 2 or 3"
        sys.exit(STATE_UNKNOWN)

    if not args['error-state'] in STATES:
        print "Error state must be 0, 1, 2 or 3"
        sys.exit(STATE_UNKNOWN)


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      'H:S:t:l:s:e:hV',
                                      ['hostname=', 'help', 'version',
                                       'latency=', 'state=', 'error-state=',
                                       'servicename=', 'type='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        if option_name in ("-S", "--servicename"):
            args['servicename'] = value
        elif option_name in ("-t", "--type"):
            args['type'] = value
        elif option_name in ("-l", "--latency"):
            args['latency'] = int(value)
        elif option_name in ("-s", "--state"):
            args['state'] = int(value)
        elif option_name in ("-e", "--error-state"):
            args['error-state'] = int(value)
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
