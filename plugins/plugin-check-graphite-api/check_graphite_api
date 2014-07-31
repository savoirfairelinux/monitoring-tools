#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This plugin is made to ensure data freshness into Graphite.
It uses the graphite API, urllib and json to get data.
Regarding the timestamp and the thresholds it returns the expected state.
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
#               check_graphite_api
#
#
#     Author: Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import getopt
import sys
import json
import urllib
import syslog

PLUGIN_NAME = "check_graphite_api"
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
Send email to <sebastien.coavoux@savoirfairelinux.com> if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to <sebastien.coavoux@savoirfairelinux.com>
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
"""
    print support_msg


def print_usage():
    """Show how to use this plugin
    """
    usage_msg = """
%s.py -u <url> -t <target> -d <delay> [-v] [-s -l <level> -f <facility>] [-C <chain>]

Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -M, --mod-plugin
    print output in stdout (or syslog) OK state. (monitoring-plugin behavior)
    Useful if you use the check with a Shinken command/service.
 -s, --syslog
    Print output into syslog. Facility and level must be specified to work
    Note : Argument parsing errors are still printed to stdout
 -l, --level=INTEGER
    Level for syslog option
 -f, --facility=INTEGER
    Facility for syslog option
 -d, --delay=STRING
    Delay to fetch data. Returns an error if no data found (default 12hours)
    Example : 12hours
 -u, --url=URL
    Url to graphite api : protocol://[user:password@]server[:port]/path
    Example : http://graphite-server/graphite/
    The plugin will add '/render/?target=TARGET_FROM_S_OPTION&from=-12hours&format=json'
    to the URL to get data
 -t, --target=STRING
    Service (or host) to get data from in the graphite way (replace special char by .)
    Example : myhost.myservice.mygraph
    Example : myhost.myservice.* (will pick only ONE dp)
 -C, --chain=STRING
    String used to know which daemons are actually checked in this the end-to-end check
    Used in case of multi poller/broker in Shinken
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """

    url = args['url'].strip("/")
    try:
        conn = urllib.urlopen("%s/render/?target=%s&from=-%s&format=json" % (url, args['target'], args['delay']))
        jdata = json.load(conn)
    except ValueError, e:
        log_message("[%(chain)s] Shinken GraphiteHealth - UNKNOWN : JSON not decoded" % args,
                    args['syslog'], args['level'], args['facility'])
        sys.exit(STATE_UNKNOWN)
    except IOError, e:
        log_message("[%s] Shinken GraphiteHealth - UNKNOWN : Cannot connect to url %s" % (args['chain'], url),
                    args['syslog'], args['level'], args['facility'])
        sys.exit(STATE_UNKNOWN)

    if len(jdata) < 1:
        log_message("[%(chain)s] Shinken GraphiteHealth - UNKNOWN : Error getting data" % args,
                    args['syslog'], args['level'], args['facility'])
        sys.exit(STATE_UNKNOWN)

    # Todo : Use it if need perfdata
    #now = time.time()

    for data in jdata:
        dp = data['datapoints']

        # Look for any not None value
        # Todo : Get timestamp for perfdata
        if [(v,t) for v,t in dp if v is not None] != []:
            if args['mod-plugin']:
                print "OK : Data found"
            sys.exit(STATE_OK)

    log_message("[%(chain)s] Shinken GraphiteHealth - CRITICAL : No data found" % args,
                args['syslog'], args['level'], args['facility'])
    sys.exit(STATE_CRITICAL)


def log_message(msg, is_syslog=False, level=None, facility=None):
    if is_syslog:
        syslog.syslog(level | facility, msg)
    else:
        print msg


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['url', 'target']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "UNKNOWN : Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if 'delay' not in args.keys():
        args['delay'] = "12hours"

    if 'mod-plugin' not in args.keys():
        args['mod-plugin'] = False

    if 'chain' not in args.keys():
        args['chain'] = None

    if 'syslog' not in args.keys():
        args['syslog'] = False
        args['level'] = None
        args['facility'] = None
    elif 'facility' not in args.keys() or 'level' not in args.keys():
        print "UNKNOWN : facility and level must be specified when using syslog option"
        print_usage()
        print_support()
        sys.exit(STATE_UNKNOWN)


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'u:hVMd:t:sl:f:C:',
                        ['url=', 'help', 'version',
                         'mod-plugin', 'delay=', 'target=',
                         'syslog', 'level=', 'facility=',
                         'chain='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-u", "--url"):
            args['url'] = value
        elif option_name in ("-d", "--delay"):
            args['delay'] = value
        elif option_name in ("-t", "--target"):
            args['target'] = value
        elif option_name in ("-s", "--syslog"):
            args['syslog'] = True
        elif option_name in ("-l", "--level"):
            args['level'] = int(value)
        elif option_name in ("-f", "--facility"):
            args['facility'] = int(value)
        elif option_name in ("-C", "--chain"):
            args['chain'] = value
        elif option_name in ("-h", "--help"):
            print_version()
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)
        elif option_name in ("-V", "--version"):
            print_version()
            print_support()
            sys.exit(STATE_UNKNOWN)
        elif option_name in ("-M", "--mod-plugin"):
            args['mod-plugin'] = True

    check_arguments(args)

    get_data(args)


if __name__ == "__main__":
    main()
