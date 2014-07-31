#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check Linksys SPA-2102 status
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
#     Projects :
#               SFL Shinken plugins
#
#     File :
#               check_spa2102 Check Linksys SPA-2102 status
#
#
#     Author: Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import getopt
import sys

PLUGIN_NAME = "check_spa2102"
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
%s.py -H <host> -w <warning> -c <critical>

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -V, --version
    Print version information
 -P, --port=INTEGER
    Port to connect to. Default 80
 -p, --page=STRING
    Page to get with http. Default /voice/
 -l, --line=INTEGER
    Hardware line to check 1 or 2
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    import httplib
    from lxml import etree
    from StringIO import StringIO

    conn = httplib.HTTPConnection(args["hostname"] + ':' + args["port"])
    try:
        conn.request("GET", args["page"])
    except Exception:
        print "CRITICAL - Can't connect to %s with %s" % (args["hostname"], args["port"])
        sys.exit(STATE_CRITICAL)
    res = conn.getresponse()
    if not res.status in [200, 302]:
        print "CRITICAL - Can't get data from the device"
        sys.exit(STATE_CRITICAL)
    data = res.read()
    parser = etree.HTMLParser()

    html = etree.parse(StringIO(data), parser)
    # The findall look for everty tg tag into the html code
    # We want the node where the text is "Registration State"
    # If you need to parse something else, just change the value.
    # In this case there are two matches : one for each hardware line
    registered_node = \
        [x for x in html.findall('//td') if x.text and x.text.startswith("Registration State")]

    # From there we want the associated value of the "Registration State"
    # We know the structure of the html code so we get the value we  need
    raw_line = args['line'] - 1
    state_registration = registered_node[raw_line].getparent().findall(".//font")[1].text

    if state_registration == "Registered":
        print "OK - Line %d : %s" % (args['line'], state_registration)
        sys.exit(STATE_OK)
    elif state_registration == "Not Registered":
        print "CRITICAL - Line %d : %s" % (args['line'], state_registration)
        sys.exit(STATE_CRITICAL)
    else:
        print "CRITICAL - Line %d : Unknown state %s" % (args['line'], state_registration)
        sys.exit(STATE_CRITICAL)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['hostname']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "UNKNOWN - Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'port' in args.keys():
        args['port'] = '80'

    if not 'page' in args.keys():
        args['page'] = '/voice/'

    if not 'line' in args.keys():
        args['line'] = 1
    elif not 1 <= args['line'] <= 2:
        print "UNKNOWN - Bad number for the line parameter line : %d" % args['line']
        sys.exit(STATE_UNKNOWN)


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:hVP:p:l:',
                        ['hostname=', 'help', 'version',
                         'port=', 'page=', 'line='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        elif option_name in ("-P", "--port"):
            args['port'] = value
        elif option_name in ("-p", "--page"):
            args['page'] = value
        elif option_name in ("-l", "--line"):
            args['line'] = int(value)
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
