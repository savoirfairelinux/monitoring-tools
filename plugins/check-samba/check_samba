#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Samba server check
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
#               check_samba Samba server check
#
#
#     Author: Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import getopt
import sys

PLUGIN_NAME = "check_samba"
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
Send email to sebastien.coavoux@savoirfairelinux.com if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to sebastien.coavoux@savoirfairelinux.com
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
"""
    print support_msg


def print_usage():
    """Show how to use this plugin
    """
    usage_msg = """
%s.py -H <host> -w <warning> -c <critical> -t <timeout> -u <user>""" \
""" -p <password> -d <domain> -s <shared-dir>

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -C, --computer=STRING
    Computer name, useful for windows computers when dns name is not the computer name
 -V, --version
    Print version information
 -w, --warning=DOUBLE
    Response time to result in warning status (seconds)
 -c, --critical=DOUBLE
    Response time to result in critical status (seconds)
 -t, --timeout=INTEGER
    Timeout to connect to server (seconds)
 -u, --username=STRING
    Username to connect to samba server
 -p, --password=STRING
    Password to connect to samba server
 -d, --domain=STRING
    Domain to conect to samba server
 -s, --shared-dir=STRING
    Name of the shared directory to check
 -n, --ntlm-v1
    Use the v1 of ntlm (default v2)
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    import time
    import socket
    from smb import SMBConnection


    start = time.time()

    ip = None
    # Check ip, if it doesn't look like a valid ipv4 then we consider it as an hostname
    try:
        socket.inet_aton(args['hostname'])
        ip = args['hostname']
    except socket.error:
        pass

    # it's an ip so we resolve the hostname
    if ip:
        try:
            args['hostname'] = socket.gethostbyaddr(args['hostname'])[0]
        except socket.error:
            print "CRITICAL - UNKNOWN Ip address : %s" % args['hostname']
            sys.exit(STATE_CRITICAL)

    if args['computer'] == '': 
        # computer name was empty so we specify it
        args['computer'] = args['hostname']


    # No we try the Samba connection
    try:
        smb = SMBConnection.SMBConnection(
            args['username'], args['password'], \
            "check_samba", args['computer'], domain=args['domain'], \
            use_ntlm_v2=args['use_ntlm_v2'], sign_options=2)

        smb.connect(args['hostname'], timeout=args['timeout'])
    except Exception:
        print "CRITICAL - Can't connect to %s" % args['hostname']
        sys.exit(STATE_CRITICAL)

    end = time.time()

    #Here we try to list file into the specified shared directory
    try:
        smb.listPath(args['shared'], '/')
    except Exception:
        print "CRITICAL - Can't list files into %s" % args['shared']
        sys.exit(STATE_CRITICAL)


    elapsed = end - start

    if not 'critical' in args.keys():
        print "OK - Everything is fine! | time=%0.3fs;;;0;%0.3f" % \
            (elapsed, args['timeout'])
        sys.exit(STATE_OK)

    #If the elapsed time to connect to Samba is too high, a CRITICAL or WARNING STATE is returned
    if elapsed > args['critical']:
        print "CRITICAL - Too long to connect to %s | time=%0.3fs;%0.3f;%0.3f;0;%0.3f" % \
            (args['hostname'], elapsed, args['warning'], args['critical'], args['timeout'])
        sys.exit(STATE_CRITICAL)
    elif args['warning'] < elapsed < args['critical']:
        print "WARNING - Too long to connect to %s | time=%0.3fs;%0.3f;%0.3f;0;%0.3f" % \
            (args['hostname'], elapsed, args['warning'], args['critical'], args['timeout'])
        sys.exit(STATE_WARNING)
    else:
        print "OK - Everything is fine! | time=%0.3fs;%0.3f;%0.3f;0;%0.3f" % \
            (elapsed, args['warning'], args['critical'], args['timeout'])
        sys.exit(STATE_OK)



def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['hostname',
                           'shared']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "UNKNOWN - Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if ('warning' in args.keys()) ^ ('critical' in args.keys()):
        print "UNKNOWN - You can't specify only warning or critical. Specify both or none of them"
        sys.exit(STATE_UNKNOWN)

    if not 'timeout' in args.keys():
        args['timeout'] = 60

    if not 'domain' in args.keys():
        args['domain'] = ''

    if not 'username' in args.keys():
        args['username'] = ''

    if not 'password' in args.keys():
        args['password'] = ''

    if not 'computer' in args.keys():
        args['computer'] = ''

    args['use_ntlm_v2'] = not 'use_ntlm_v2' in args.keys()

    if ('warning' in args.keys() and 'critical' in args.keys() and \
        args['warning'] > args['critical']
        )or(
        'warning' in args.keys() and 'critical' in args.keys() and 'timeout' in args.keys() and \
        not args['warning'] <= args['critical'] <= args['timeout']):
            print "UNKNOWN - Wrong warning, critical or timeout values."\
                "Please ensure warning<critical<timeout"
            sys.exit(STATE_UNKNOWN)


def main():
    """Main function
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:hVw:c:t:u:p:d:s:nC:',
                        ['hostname=', 'help', 'version',
                         'warning=', 'critical=', 'timeout=',
                         'username=', 'password=', 'domain=',
                         'share=', 'ntlm-v1', 'computer='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        elif option_name in ("-C", "--computer"):
            args['computer'] = value
        elif option_name in ("-w", "--warning"):
            args['warning'] = float(value)
        elif option_name in ("-c", "--critical"):
            args['critical'] = float(value)
        elif option_name in ("-t", "--timeout"):
            args['timeout'] = int(value)
        elif option_name in ("-u", "--username"):
            args['username'] = value
        elif option_name in ("-p", "--password"):
            args['password'] = value
        elif option_name in ("-d", "--domain"):
            args['domain'] = value
        elif option_name in ("-s", "--shared-dir"):
            args['shared'] = value
        elif option_name in ("-n", "--ntlm-v1"):
            args['use_ntlm_v2'] = False
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
