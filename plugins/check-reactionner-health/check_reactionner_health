#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pseudo crontab to check if a file is edited by shinken reactionner
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
#               check_reactionner_health Pseudo crontab to check if a file is edited by shinken reactionner
#
#
#     Author: Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import getopt
import sys
import syslog
import os
import time
import subprocess

PLUGIN_NAME = "check_reactionner_health"
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
%s.py -m <max-age> -p <path> [-s -l <level> -f <facility>] [-C <chain>] [-V] [-h] [-P]

Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -p, --path=STRING
    Path to file to check
 -m, --max-age=DOUBLE
    maximum age for file (based on last edit) in minutes
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
 -C, --chain=STRING
    String used to know which daemons are actually checked in this the end-to-end check
    Used in case of multi poller/broker in Shinken
 -r, --remote-shell=IP
    If specified, this will check a file on the remote IP. You need to allow ssh access on the IP
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """

    if 'remote-shell' in args.keys():
        proc_pipe = subprocess.Popen(["ssh",
                                      "shinken@%s" % args['remote-shell'],
                                      "-C",
                                      "stat -c %%Y %s" % args['path']],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        err = proc_pipe.stderr.read()
        # Todo show the right error : no file or permission denied
        if err != '':
            log_message("[%(chain)s] Shinken ReactionnerHealth - CRITICAL : File not found" % args,
                        args['syslog'], args['level'], args['facility'])
            sys.exit(STATE_CRITICAL)

        timestamp = int(proc_pipe.stdout.read())
        diff = time.time() - timestamp
    else:
        try:
            diff = time.time() - os.stat(args['path']).st_mtime
        except OSError:
            # Todo show the right error : no file or permission denied
            log_message("[%(chain)s] Shinken ReactionnerHealth - CRITICAL : File not found" % args,
                        args['syslog'], args['level'], args['facility'])
            sys.exit(STATE_CRITICAL)

    if diff > args['max-age'] * 60:
        log_message("[%(chain)s] Shinken ReactionnerHealth - CRITICAL : File %(path)s is too old" % args,
                    args['syslog'], args['level'], args['facility'])
        sys.exit(STATE_CRITICAL)
    else:
        #Not implemented for now
        if args['mod-plugin']:
            pass
        sys.exit(STATE_OK)


def log_message(msg, to_syslog=False, level=None, facility=None):
    if to_syslog:
        syslog.syslog(level | facility, msg)
    else:
        print msg


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['path',
                           'max-age']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "UNKNOWN : Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

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
    """Main function
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'hVMp:m:sl:f:C:r:',
                        ['path=', 'help', 'version', 'mod-plugin', 'max-age=',
                         'syslog', 'level=', 'facility=', 'chain=', 'remote-shell='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-p", "--path"):
            args['path'] = value
        elif option_name in ("-m", "--max-age"):
            args['max-age'] = float(value)
        elif option_name in ("-M", "--mod-plugin"):
            args['mod-plugin'] = True
        elif option_name in ("-s", "--syslog"):
            args['syslog'] = True
        elif option_name in ("-l", "--level"):
            args['level'] = int(value)
        elif option_name in ("-f", "--facility"):
            args['facility'] = int(value)
        elif option_name in ("-C", "--chain"):
            args['chain'] = value
        elif option_name in ("-r", "--remote-shell"):
            args['remote-shell'] = value
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
