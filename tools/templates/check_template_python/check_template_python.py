#!/usr/bin/python
# -*- coding: utf-8 -*-
"""<description>
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
#               check_template_python.py <description>
#
#
#     Author: <author_name> <<author_email>>
#
#

import getopt
import sys

PLUGIN_NAME = "check_template_python"
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
Send email to <<author_email>> if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to <<author_email>>
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
"""
    print support_msg


def print_usage():
    """Show how to use this plugin
    """
    usage_msg = """
%s.py -H <host> -w <warning> -c <critical>

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -V, --version
    Print version information
 -w, --warning=DOUBLE
    Response time to result in warning status (seconds)
 -c, --critical=DOUBLE
    Response time to result in critical status (seconds)
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    import datetime
    now = datetime.datetime.now()
    minute = now.minute
    hour = now.hour
    if minute % 2:
        test_data = "WARNING - time : %d:%d |minute=%d;0;60;" % \
                                        (hour, minute, minute)
    elif minute % 3:
        test_data = "CRITICAL - time : %d:%d |minute=%d;0;60;" % \
                                        (hour, minute, minute)
    else:
        test_data = "OK - time : %d:%d | minute=%d;0;60;" % \
                                        (hour, minute, minute)

    print test_data

    if minute > args['critical']:
        sys.exit(STATE_CRITICAL)
    elif minute > args['warning']:
        sys.exit(STATE_WARNING)
    else:
        sys.exit(STATE_OK)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['warning',
                           'critical']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'hostname' in args.keys():
        args['hostname'] = '127.0.0.1'


def main():
    """Main function
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:hVw:c:',
                        ['hostname=', 'help', 'version',
                         'warning=', 'critical='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        elif option_name in ("-w", "--warning"):
            args['warning'] = value
        elif option_name in ("-c", "--critical"):
            args['critical'] = value
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
