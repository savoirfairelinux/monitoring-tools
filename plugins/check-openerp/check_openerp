#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check OpenERP using a web scenario
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
#               check_openerp Check OpenERP using a web scenario
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
import json
import httplib
import time

PLUGIN_NAME = "check_openerp"
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
Send email to <thibault.cohen@savoirfairelinux.com> if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to <thibault.cohen@savoirfairelinux.com>
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
"""
    print support_msg


def print_usage():
    """Show how to use this plugin
    """
    usage_msg = """
%s.py -H <host> -w <warning> -c <critical> -d <database_name> -u <username> -p <password> [-P <port>] [-S] [-U <uid>] [-V] [-h]

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -P, --port=PORT
    http port
 -S, --ssl
    Use HTTPS => default port 443
 -u, --username
    Username
 -p, --password
    Pasword
 -d, --database
    Database name
 -U, --uid
    User databases UID
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
    # Start timer
    start_time = time.time()
    # Get home page
    home_url = args['hostname']
    if args['ssl'] == True:
        con = httplib.HTTPSConnection(home_url, args['port'])
        args['scheme'] = "https"
    else:
        con = httplib.HTTPConnection(home_url, args['port'])
        args['scheme'] = "http"
    args['url'] = "://".join((args['scheme'], args['hostname'] + "/"))
    try:
        con.request("GET", "/")
    except Exception, e:
        print "CRITICAL: Error on '%s': %s" % (args['url'], e)
        sys.exit(STATE_CRITICAL)
        
    response = con.getresponse()

    # Check response
    if response.status != 200:
        args['status'] = response.status
        print "CRITICAL: %(url)s: %(scheme)s status code: %(status)d (expected: 200)" % args
        sys.exit(STATE_CRITICAL)
    res_1 = response.read()
    
    # Get session info
    get_session_url = "/web/session/get_session_info"
    args['url'] = "://".join((args['scheme'], args['hostname'] + get_session_url))
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data_dict_2 = {"jsonrpc": "2.0",
                   "method": "call",
                   "params": {"session_id": None,
                              "context":{},
                             },
                   "id":"r0",
                  }
    try:
        con.request("POST", get_session_url, json.dumps(data_dict_2), headers)
    except Exception, e:
        print "CRITICAL: Error on '%s': %s" % (args['url'], e)
        sys.exit(STATE_CRITICAL)

    response = con.getresponse()

    # Check response
    if response.status != 200:
        args['status'] = response.status
        print "%(url)s: HTTPs status code: %(status)d (expected: 200)" % args
        sys.exit(STATE_CRITICAL)
    try:
        res_data_2 = json.load(response)
    except:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)
    if not 'result' in res_data_2:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)
    if not 'session_id' in res_data_2['result']:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)

    # Login
    data_dict_3 = {"jsonrpc": "2.0",
                   "method": "call",
                   "params": {"db": args['database'],
                              "login": args['username'],
                              "password": args['password'],
                              "base_location": args['hostname'],
                              "session_id": res_data_2['result']['session_id'],
                              "context": {},
                             },
                   "id":"r6",
                  }
    login_url = "/web/session/authenticate"
    args['url'] = "://".join((args['scheme'], args['hostname'] + login_url))
    try:
        con.request("POST", login_url, json.dumps(data_dict_3), headers)
    except Exception, e:
        print "CRITICAL: Error on '%s': %s" % (args['url'], e)
        sys.exit(STATE_CRITICAL)

    response = con.getresponse()

    # Check response
    if response.status != 200:
        args['status'] = response.status
        print "CRITICAL: %(url)s: HTTP status code: %(status)d (expected: 200)" % args
        sys.exit(STATE_CRITICAL)
    try:
        res_data_3 = json.load(response)
    except:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)

    # Get parf data
    args['time'] = time.time() - start_time
    perf_msg = "time:%(time)0.2fs;%(warning)d;%(critical)d;0;" % args

    # Check response
    if not 'result' in res_data_3:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)
    if not 'user_context' in res_data_3['result']:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)
    if 'uid' in res_data_3['result'] and res_data_3['result']['uid'] == False:
        message = "CRITICAL: Login failed on %(scheme)s://%(hostname)s" % args
        print " | ".join((message, perf_msg))
        sys.exit(STATE_CRITICAL)
    if not 'uid' in res_data_3['result']['user_context']:
        print "CRITICAL: Bad HTTP response from %(url)s" % args
        sys.exit(STATE_CRITICAL)


    # Compare UID
    args['uid_found'] = res_data_3['result']['user_context']['uid']
    if not args['uid'] is None:
        if args['uid_found'] != args['uid']:
            message = "WARNING: Login error on %(url)s: Bad UID found: %(uid_found)d (expected: %(uid)d)" % args
            print " | ".join((message, perf_msg))
            sys.exit(STATE_WARNING)

    elif args['uid_found'] == False:
        message = "CRITICAL: Login failed at %(url)s" %s
        print " | ".join((message, perf_msg))
        sys.exit(STATE_CRITICAL)

    # Compare time
    if args['time'] > args['critical']:
        message = "CRITICAL: OpenERP (%(scheme)s://%(hostname)s) seems really slow (connection time: %(time)0.2fs)" % args
        print " | ".join((message, perf_msg))
        sys.exit(STATE_CRITICAL)
    elif args['time'] > args['warning']:
        message = "WARNING: OpenERP (%(scheme)s://%(hostname)s) seems slow (connection time: %(time)0.2fs)" % args
        print " | ".join((message, perf_msg))
        sys.exit(STATE_WARNING)
    else:
        message = "OK: OpenERP (%(scheme)s://%(hostname)s) looks good (connection time: %(time)0.2fs)" % args
        print " | ".join((message, perf_msg))
        sys.exit(STATE_OK)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = [
                            'hostname',
                            'username',
                            'password',
                            'warning',
                            'critical',
                            'database',
                           ]
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    float_arguments = [
                     'warning',
                     'critical',
                     'uid',
                    ]
    for argument_name in float_arguments:
        try:
            if argument_name in args:
                args[argument_name] = float(args[argument_name])
        except:
            print "Bad format for argument '%s' !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'uid' in args:
        args['uid'] = None

    if not 'ssl' in args:
        args['ssl'] = False

    if not 'port' in args and args['ssl'] == True:
        args['port'] = 443
    elif not 'port' in args and args['ssl'] == False:
        args['port'] = 80


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:P:ShVw:c:u:p:U:d:',
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
        if option_name in ("-u", "--username"):
            args['username'] = value
        if option_name in ("-p", "--password"):
            args['password'] = value
        if option_name in ("-d", "--database"):
            args['database'] = value
        if option_name in ("-U", "--uid"):
            args['uid'] = value
        if option_name in ("-S", "--ssl"):
            args['ssl'] = True
        if option_name in ("-P", "--port"):
            args['port'] = int(value)
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
