#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check channels in error with wanpipe
"""
#
#
#     Copyright (C) 2013 Savoir-Faire Linux Inc.
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
#               check_wanpipe Check channels in error with wanpipe
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
import os
import re
import subprocess
import time


PLUGIN_NAME = "check_wanpipe"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4

WANPIPEMON = '/usr/sbin/wanpipemon'


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
%s -H <hostname> -S <servicename> -t <type> [-l <latency>]\
 [-s <state>] [-e <error-state>]

perfdata',
                                       'interface=', 'channels=',
                                       'critical=', 'warning=
Usage:
 -h, --help
    Print detailed help screen
 -c, --channels=NUMBEROFCHANNELS
    Precise the number of channels
 -i, --interfacename=INTERFACENAME
    Interface name
    Default: w1g1
 -w, --warning=WARNING
    Number of 
    Plugin latency, fake slow plugin ...
    Default: 0
 -c, --state=STATE
    State in normal mode : 0 (OK), 1 (WARNING), 2 (CRITICAL), 3 (UNKNOWN)
    Default: 0
 -f, --perfdata
    add perfdata to the output
    Default: False
 -V, --version
    Print version information
""" % PLUGIN_NAME
    print usage_msg


def get_data(kargs):
    """Fetch data
    """
    warning = kargs['warning']
    critical = kargs['critical']
    interface = kargs['interface']
    channels = kargs['channels']
    perfdata = kargs['perfdata']

    results = {}
    for channel in xrange(1, channels + 1):
        # if not sleep, it may not get value
        time.sleep(0.4)
        # Launch command
        if not kargs['in_test']:
            s = subprocess.Popen('sudo '
                                 + WANPIPEMON +
                                 ' -i '
                                 + interface +
                                 ' -c astats -m '
                                 + str(channel),
                                 shell=True, stdout=subprocess.PIPE)
            output = s.stdout
        else:
            output = open(os.path.join(os.getcwd(), 'test_output%s' % channel))


        for line in output.readlines():
            # Set default state (0:ok, 1:bad)
            state = 1
            # Clean line
            line = line.strip()
            # Empty line ...
            if not line:
                continue
            # Get port number
            result = re.search('port ([0-9]*)', line)
            if result:
                port = result.groups()[0]
                continue
            # Get voltage
            result = re.search('VOLTAGE\t: ([0-9]*) Volts', line)
            if result:
                volt = result.groups()[0]
                try:
                    volt = int(volt)
                    if volt < 5:
                        state = 1
                    else:
                        state = 0
                except:
                    state = 1
                results[port] = state
                continue
    # Process result
    if len(results) == 0:
        errors = channels
    else: 
        errors = sum(results.values()) + channels - len(results)
    available_channels = channels - errors
    if errors > 0:
        msg = '%s/%s channels in OK state' % (available_channels, channels)
    else:
        msg = 'All of %s channels are in OK state' % channels

    if perfdata:
        if critical > -1 and warning > -1:
            perfdata = ('available_channels=' + str(available_channels) + 'channels'
                        ';' + str(warning) + ';' + str(critical) + ';0;'
                        + str(channels) )
        else:
            perfdata = ('available_channels=' + str(available_channels) + 'channels'
                        ';;;0;' + str(channels) )
        msg = msg + " | " + perfdata

    if critical > -1 and warning > -1:
        if available_channels <= critical:
            msg = "CRITICAL - " + msg
            exit_code = STATE_CRITICAL
        elif available_channels <= warning:
            msg = "WARNING - " + msg
            exit_code = STATE_WARNING
        else:
            msg = "OK - " + msg
            exit_code = STATE_OK
    else:
            msg = "OK - " + msg
            exit_code = STATE_OK
    print msg
    sys.exit(exit_code)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['channels',
                           ]
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument `%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'warning' in args.keys():
        args['warning'] = -1

    if not 'critical' in args.keys():
        args['critical'] = -1

    if not 'interface' in args.keys():
        args['interface'] = "w1g1"

    if not 'perfdata' in args.keys():
        args['perfdata'] = False

    int_arguments = [
                       'channels',
                       'warning',
                       'critical',
                        ]
    for argument_name in int_arguments:
        if argument_name in args:
            try:
                args[argument_name] = int(args[argument_name])
            except:
                print "Bad format for argument: %s !" % argument_name
                print_support()
                sys.exit(STATE_UNKNOWN)

    if args['warning'] < args['critical']:
        print "Warning argument but be greater than critical argument"
        print_support()
        sys.exit(STATE_UNKNOWN)

    return args


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      'hVfi:s:c:w:',
                                      ['help', 'version', 'perfdata',
                                       'interface=', 'channels=',
                                       'critical=', 'warning='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {'in_test': False}
    # Detect if nosetests if running
    if sys.argv[0].endswith('nosetests'):
        args['in_test'] = True

    for option_name, value in options:
        if option_name in ("-i", "--interface"):
            args['interface'] = value
        if option_name in ("-s", "--channels"):
            args['channels'] = value
        elif option_name in ("-w", "--warning"):
            args['warning'] = value
        elif option_name in ("-c", "--critical"):
            args['critical'] = value
        elif option_name in ("-f", "--perfdata"):
            args['perfdata'] = True
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
