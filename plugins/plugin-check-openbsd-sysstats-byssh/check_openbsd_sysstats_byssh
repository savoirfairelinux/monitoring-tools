#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check OpenBSD system stats
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
#               check_carp_by_ssh.py Check carp status on Soekris using ssh
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

PLUGIN_NAME = "check_openbsd_sysstats_byssh"
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
%s.py -H <address> -w <warning> -c <critical>

You must create a user shinken/nagios on openbsd host
And create ssh key and share it and add ssh pub key of 
the shinken server in openbsd hosts...
 
Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -H, --hostname=ADDRESS
    Hostname or IP
 -w, --load-warning=load1:load5:load15
    Warning load threshold
 -c, --load-critical=load1:load5:load15
    Critical load threshold

""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    if not args['in_test']:
        process = Popen("ssh -o ConnectTimeout=5 "
                               + args['hostname'] +
                               " top -b ",
                               shell=True,
                               stdout=PIPE,
                               stderr=STDOUT)
        output, stderr = process.communicate()
        status = process.poll()
    else:
        # In test
        foutput = open(os.path.join(os.getcwd(), args['hostname'] + ".txt"))
        output = foutput.read()
        status = 0

    if status != 0:
        print "ERROR while fetching data"
        sys.exit(STATE_UNKNOWN)
       
    raw_load_stats = output.splitlines()[0]
    raw_cpu_stats = output.splitlines()[2]
    raw_mem_stats = output.splitlines()[3]
    results = {'load': {},
               'cpu': {},
               'memory': {},
               'swap': {},
                }
    # LOAD
    try:
        l1, l5, l15 = re.match('load averages:[ ]*([0-9\.]*),[ ]*([0-9\.]*),[ ]*([0-9\.]*)', raw_load_stats).groups()
        results['load']['load_1'] = (l1, '')
        results['load']['load_5'] = (l5, '')
        results['load']['load_15'] = (l15, '')
    except:
        pass
    # CPU
    try:
        raw_cpu_stats = re.match('CPU states:[ ]*([0-9\.\% a-z]*),[ ]*([0-9\.\% a-z]*),[ ]*([0-9\.\% a-z]*),[ ]*([0-9\.\% a-z]*),[ ]*([0-9\.\% a-z]*)', raw_cpu_stats).groups()
        for stat in raw_cpu_stats:
            value, unit, name = re.match('([0-9\.]*)([%]) ([a-zA-Z]*)', stat).groups()
            results['cpu'][name] = (value, unit)
    except:
        pass
    # MEM
    try:
        raw_mem_stats = re.match('Memory: Real:([0-9a-zA-Z\/ ]*)Free:([0-9a-zA-Z\/ ]*)Swap:([0-9a-zA-Z\/ ]*)', raw_mem_stats).groups()
        # USED
        _, _, d, u, _, _ = re.match('([0-9]*)([a-zA-Z])/([0-9]*)([a-zA-Z]) ([a-zA-Z]*)/([a-zA-Z]*)', raw_mem_stats[0].strip()).groups()
        results['memory']['used'] = (int(d), u)
        # FREE
        d, u = re.match('([0-9]*)([a-zA-Z])', raw_mem_stats[1].strip()).groups()
        results['memory']['free'] = (int(d), u)
        results['memory']['total'] = (results['memory']['free'][0] + results['memory']['used'][0],
                                      results['memory']['free'][1])
        # SWAP
        d1, u1, d2, u2, _, _ = re.match('([0-9]*)([a-zA-Z])/([0-9]*)([a-zA-Z]) ([a-zA-Z]*)/([a-zA-Z]*)', raw_mem_stats[2].strip()).groups()
        results['swap']['used'] = (int(d1), u1)
        results['swap']['total'] = (int(d2), u2)
    except:
        pass

    # Format results
    perf = ''
    msg = []
    for name, datas in results.items():
        f_data = {}
        f_data['data_name'] = name.capitalize()
        for s_name, data in datas.items():
            if s_name == 'total':
                continue
            f_data['name'] = s_name
            f_data['value'] = float(data[0])
            f_data['unit'] = data[1]
            f_data['max'] = ''
            if 'total' in datas:
                f_data['max'] = "%0.2f" % float(datas['total'][0])
            elif f_data['unit'] == "%":
                f_data['max'] = '100.00'
            perf += " %(name)s=%(value)0.2f%(unit)s;;;0.00;%(max)s" % f_data

            if s_name in ['load_15', 'free', 'idle']:
                msg.append("%(data_name)s %(name)s: %(value)s%(unit)s" % f_data)


    exit_code = STATE_OK
    exit_code_mapping = {
                    'warning': STATE_WARNING,
                    'critical': STATE_CRITICAL,
                    }
    msg_prefix = 'OK'

    # loop on warning, critical
    for type_, ts in args['thresholds'].items():
        # loop on thresholds
        for data_type_name, ts in args['thresholds'][type_].items():
            if data_type_name in results:
                # loop results
                for ts_name, ts_data in ts.items():
                    # Get result
                    if ts_name in results[data_type_name]:
                        data = results[data_type_name][ts_name][0]
                        # Compare
                        if float(data) > float(ts_data):
                            # Get exit code
                            if exit_code_mapping[type_] > exit_code:
                                exit_code = exit_code_mapping[type_] 
                                msg_prefix = type_.upper()
    
    msg = [msg_prefix] + msg
    msg = " |".join((" - ".join(msg), perf))
    print msg

    sys.exit(exit_code)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['hostname',
                            ]
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument `%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    for t in ['load', 'cpu', 'memory', 'swap']:
        if bool(t + '_warning' in args) != bool(t + '_critical' in args):
            print "Warning and Critical %s thresholds must be define" % t.upper()
            sys.exit(STATE_UNKNOWN)

    args['thresholds'] = {}
    if 'load_warning' in args:
        for ts in ['load_warning', 'load_critical']:
            data_type, type_ = ts.split("_")
            args['thresholds'][type_] = {}
            if not re.match("([0-9\.]*),([0-9\.]*),([0-9\.]*)", args[ts]):
                print "Bad format: Warning and Critical Load thresholds"
                sys.exit(STATE_UNKNOWN)
            load_1, load_5, load_15 = re.match("([0-9\.]*),([0-9\.]*),([0-9\.]*)", args[ts]).groups()
            args['thresholds'][type_][data_type] = {}
            args['thresholds'][type_][data_type]['load_1'] = load_1
            args['thresholds'][type_][data_type]['load_5'] = load_5
            args['thresholds'][type_][data_type]['load_15'] = load_15


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'hVH:',
                        ['hostname=',
                         'load-warning=', 'load-critical=',
                         'cpu-warning=', 'cpu-critical=',
                         'mem-warning=', 'mem-critical=',
                         'swap-warning=', 'swap-critical=',
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
        if option_name in ("-H", "--hostaddress"):
            args['hostname'] = value
        elif option_name in ("---load-warning"):
            args['load_warning'] = value
        elif option_name in ("--load-critical"):
            args['load_critical'] = value
        elif option_name in ("--cpu-warning"):
            args['cpu_warning'] = value
        elif option_name in ("--cpu-critical"):
            args['cpu_critical'] = value
        elif option_name in ("--memory-warning"):
            args['memory_warning'] = value
        elif option_name in ("--memory-critical"):
            args['memory_critical'] = value
        elif option_name in ("--swap-warning"):
            args['swap_warning'] = value
        elif option_name in ("--swap-critical"):
            args['swap_critical'] = value
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
