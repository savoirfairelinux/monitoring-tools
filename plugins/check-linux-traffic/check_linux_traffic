#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check traffic on linux hosts using _proc_net_dev
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
#       check_linux_traffic Check traffic on linux hosts using _proc_net_dev
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
import time
import re
import os

PLUGIN_NAME = "check_linux_traffic"
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
%s.py [-w <warning> -c <critical>] [-l <limit>] [-n <ifname>] [-v] [-f]

Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -w, --warning=DOUBLE
    Percent warning threshold
    default: disabled
 -c, --critical=DOUBLE
    Percent critical threshold
    default: disabled
 -l, --limit=DOUBLE
    Set your bandwidth limit in B/s
    default: autodetect
 -n, --ifname=name
    Regex to search interface name
    Default: Show all interface
 --ignore-lo
    Ignore loopback interface
    Equal to : -n '^(?!lo)'
    Default: False
 -f, --perfdata
    Show perfdata in output
    Default: False

""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    exit_code = STATE_OK

    f = open('/proc/net/dev', 'r')
    data = f.read()
    f.close()
    raw = {}
    for line in data.replace("|", " ").splitlines()[2:]:
        line = [x for x in line.replace(":", " ").split(" ") if x]
        # Get datas
        inface = line[0]
        in_bytes = line[1]
        out_bytes = line[2]
        # Prepare dict
        if not inface in raw:
            raw[inface] = {}
        # Get in
        raw[inface]['in_bytes'] = float(in_bytes)
        # Get out
        raw[inface]['out_bytes'] = float(out_bytes)

    # Filter ifname
    if args['ifname']:
        for inface in raw.keys():
            if not re.search(args['ifname'], inface):
                del(raw[inface])

    # Interface not found
    if len(raw) == 0:
        print "Interface not found"
        sys.exit(STATE_UNKNOWN)

    # Ignore loopback
    if args['ignore_lo']:
        for inface in raw.keys():
            if not re.search("^(?!lo)", inface):
                del(raw[inface])

    # Init results
    results = {}
    # Get old data
    if not os.path.exists("/tmp/check_linux_traffic"):
        os.mkdir("/tmp/check_linux_traffic")
    now = int(time.time())
    data_not_ready = False
    for ifname in raw.keys():
        filename = "/tmp/check_linux_traffic/%s" % ifname
        if os.path.exists(filename):
            f = open(filename, 'r')
            old_data = f.read()
            timestamp, in_bytes, out_bytes = old_data.split(";")
            delta_time = now - int(timestamp)
            try:
                in_bytes = (raw[ifname]['in_bytes'] - float(in_bytes)) \
                            / delta_time
                out_bytes = (raw[ifname]['out_bytes'] - float(out_bytes)) \
                             / delta_time
            except ZeroDivisionError:
                print "Division by zero... interval check to small"
                sys.exit(STATE_UNKNOWN)
            f.seek(0)
        else:
            data_not_ready = True

        f.close()
        try:
            f = open(filename, 'w')
        except IOError:
            print "Could not open this file: %s" % filename
            sys.exit(STATE_UNKNOWN)
        
        # Save new_data
        f.write(";".join((str(now),
                          str(raw[ifname]['in_bytes']),
                          str(raw[ifname]['out_bytes'])
                        ))
                )
        f.close()
        # Set data in results
        results[ifname] = {}
        results[ifname]['in_bytes'] = float(in_bytes)
        results[ifname]['out_bytes'] = float(out_bytes)

    if data_not_ready:
        print "Waiting next check to get data..."
        sys.exit(STATE_OK)

    # Prepare data
    msg = []
    perfdata = []
    for ifname, values in results.items():
        warning = ''
        critical = ''
        limit = ''
        tmp_dict = {'ifname':  ifname,
                    'in_bytes': float(values['in_bytes']),
                    'out_bytes': float(values['out_bytes']),
                    'warning': warning,
                    'critical': critical,
                    'limit': limit,
                    }
        # Get limit
        if not args['limit']:
            try:
                f = open('/sys/class/net/%s/speed' % ifname, 'r')
                tmp_dict['limit'] = f.read()
                f.close()
                tmp_dict['limit'] = float(tmp_dict['limit']) * 1024 * 1024 / 8.0
            except:
                tmp_dict['limit'] = ''
                tmp_dict['warning'] = ''
                tmp_dict['critical'] = ''
        else:
            tmp_dict['limit'] = args['limit']

        if tmp_dict['limit']:
            tmp_dict['in_prct'] = float(values['in_bytes']) / float(tmp_dict['limit']) * 100.0
            tmp_dict['out_prct'] = float(values['out_bytes']) / float(tmp_dict['limit']) * 100.0

        if tmp_dict['limit'] and args['warning'] and args['critical']:
            tmp_dict['warning'] = args['warning'] * float(tmp_dict['limit']) / 100.0
            tmp_dict['critical'] = args['critical'] * float(tmp_dict['limit']) / 100.0
            tmp_dict['warning_prct'] = args['warning']
            tmp_dict['critical_prct'] = args['critical']

        #Format data G/M/K/...
        if 'in_prct' in tmp_dict and 'out_prct' in tmp_dict:
            tmp_dict['in_prct_txt'] = "(%0.2f%%)" % tmp_dict['in_prct']
            tmp_dict['out_prct_txt'] = "(%0.2f%%)" % tmp_dict['out_prct']
        else:
            tmp_dict['in_prct_txt'] = ""
            tmp_dict['out_prct_txt'] = ""

        # Prepare output
        speeds = ['B/s', 'KiB/s', 'MiB/s', 'GiB/s']

        for s in ['in', 'out']:
            i = 0
            tmp_dict[s] = tmp_dict[s + '_bytes']
            while tmp_dict[s] > 1024 and i < len(speeds) - 1:
                tmp_dict[s] = tmp_dict[s] / 1024.0
                i += 1
            tmp_dict[s + '_speed'] = speeds[i]

        msg.append("%(ifname)s: IN:%(in)0.2f%(in_speed)s%(in_prct_txt)s - "
                   "OUT:%(out)0.2f%(out_speed)s%(out_prct_txt)s" % tmp_dict)

        # GET PERFADATA
        if args['perfdata']:
            if len(results.items()) == 1:
                tmp_dict['ifname'] = ''
            else:
                tmp_dict['ifname'] = tmp_dict['ifname'] + "_"
            # Process threshold
            if tmp_dict['limit'] and args['warning'] and args['critical']:
                perfdata.append("%(ifname)sin=%(in_bytes)0.2fB/s;%(warning)0.2f;"
                            "%(critical)0.2f;0.0;%(limit)0.2f "
                            "%(ifname)sout=%(out_bytes)0.2fB/s;%(warning)0.2f;"
                            "%(critical)0.2f;0.0;%(limit)0.2f "
                            "%(ifname)sin_prct=%(in_prct)0.2f%%;"
                            "%(warning_prct)0.2f;"
                            "%(critical_prct)0.2f;0.0;100.0 "
                            "%(ifname)sout_prct=%(out_prct)0.2f%%;"
                            "%(warning_prct)0.2f;"
                            "%(critical_prct)0.2f;0.0;100.0"
                            % tmp_dict)
            elif tmp_dict['limit']:
                perfdata.append("%(ifname)sin=%(in_bytes)0.2fB/s;;"
                            ";0.0;%(limit)0.2f "
                            "%(ifname)sout=%(out_bytes)0.2fB/s;;"
                            ";0.0;%(limit)0.2f "
                            "%(ifname)sin_prct=%(in_prct)0.2f%%;"
                            ";;0.0;100.0 "
                            "%(ifname)sout_prct=%(out_prct)0.2f%%;"
                            ";;0.0;100.0"
                            % tmp_dict)
            else:
                perfdata.append("%(ifname)sin=%(in_bytes)0.2fB/s;%(warning)s;"
                            "%(critical)s;0.0;%(limit)s "
                            "%(ifname)sout=%(out_bytes)0.2fB/s;%(warning)s;"
                            "%(critical)s;0.0;%(limit)s"
                            % tmp_dict)
        # GET EXIT CODE
        if tmp_dict['in_bytes'] >= tmp_dict['critical'] \
                or tmp_dict['out_bytes'] >= tmp_dict['critical'] \
                and exit_code < STATE_CRITICAL:
            exit_code = STATE_CRITICAL
        elif (tmp_dict['in_bytes'] >= tmp_dict['warning']
                or tmp_dict['out_bytes'] >= tmp_dict['warning']) \
                and exit_code < STATE_WARNING:
            exit_code = STATE_WARNING

    if args['perfdata']:
        msg = " ; ".join(msg) + " | " + " ".join(perfdata)
    else:
        msg = " ; ".join(msg)

    if exit_code == STATE_CRITICAL:
        msg = "CRITICAL ; " + msg
    elif exit_code == STATE_WARNING:
        msg = "WARNING ; " + msg
    else:
        msg = "OK ; " + msg

    print msg
    sys.exit(exit_code)


def check_arguments(args):
    """Check mandatory fields
    """

    float_arguments = [
                       'limit',
                       'warning',
                       'critical',
                        ]
    for argument_name in float_arguments:
        if argument_name in args:
            try:
                args[argument_name] = float(args[argument_name])
            except:
                print "Bad argument: %s !" % argument_name
                print_support()
                sys.exit(STATE_UNKNOWN)

    if bool('warning' in args) != bool('critical' in args):
        print "Critical threshold and warning threshold must be define"
        print_support()
        sys.exit(STATE_UNKNOWN)

    if not 'perfdata' in args.keys():
        args['perfdata'] = False

    if not 'warning' in args.keys():
        args['warning'] = None

    if not 'critical' in args.keys():
        args['critical'] = None

    if not 'ifname' in args.keys():
        args['ifname'] = None

    if not 'limit' in args.keys():
        args['limit'] = None

    if not 'ignore_lo' in args.keys():
        args['ignore_lo'] = False

    if args['warning'] > args['critical']:
        print "Critical threshold must be greater than warning threshold"
        print_support()
        sys.exit(STATE_UNKNOWN)

    return args


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'hVl:n:w:c:f',
                        ['help', 'version', 'ignore-lo',
                         'limit=', 'perfdata', 'ifname=',
                         'warning=', 'critical='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-w", "--warning"):
            args['warning'] = value
        elif option_name in ("-c", "--critical"):
            args['critical'] = value
        elif option_name in ("-l", "--limit"):
            args['limit'] = value
        elif option_name in ("-n", "--ifname"):
            args['ifname'] = value
        elif option_name in ("--ignore-lo"):
            args['ignore_lo'] = True
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

    args = check_arguments(args)

    get_data(args)


if __name__ == "__main__":
    main()
