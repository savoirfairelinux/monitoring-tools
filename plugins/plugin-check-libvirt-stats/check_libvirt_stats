#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Guest and host statistics from libvirt API
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
#               check_libvirt_stats Guest and host statistics from libvirt API
#
#
#     Author: Jean Rémond <jean.remond@savoirfairelinux.com>
#
#


# TODO
# handle : libvirt.libvirtError: End of file while reading data: : Input/output error => Check shinken.nagios default shell (NOT bin/false)
import getopt
import sys
from urlparse import urlparse

import libvirtstat

PLUGIN_NAME = "check_libvirt_stats"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4

UNITS = {'Mb': 0,
         'MB': 0,
         'Gb': 1,
         'GB': 1,
         'TB': 2,
         'Tb': 2,
        }
LIBVIRT_PROTOCOLS = ('qemu', 'xen', 'xenapi', 'uml', 'lxc', 'test',
                     'vbox', 'openvz', 'esx', 'one', 'phyp')

# Transport
# tls tcp, unix, ssh and ext.
# If omitted, it will default to tls if a hostname is provided,
# or unix if no hostname is provided.
LIBVIRT_TRANSPORTS = ('tls', 'tcp', 'unix', 'ssh', 'ext')



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
%s.py -u <uri> [-U <unit>] [-w <warning> -c <critical>]

Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -u, --uri=URI
    URI to access hypervisor
    example: qemu+ssh://shinken@192.168.1.1/system
 -U, --unit=[MGT][bB]
    unit to interpret values
 -w, --warning=PERCENTAGE
    Warning threshold for unit utilisation in percentage
    example: 80%%
 -c, --critical=PERCENTAGE
    Critical threshold for unit utilisation in percentage
    example: 90%%


Examples:
 check_libvirt_stats -u qemu:///system -U GB -w 80%% -c 90%% 
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """

    hypv_data = libvirtstat.list_vm_info(args['uri'])
    hypv_sorted_data = sorted([(m, data ) for m, data in hypv_data.items()],
                              key=lambda x: x[1]['state'],
                              reverse=True)

    max_memory = 0
    memory     = 0
    memory_up  = 0
    disk       = 0
    disk_up    = 0

    for vm in hypv_sorted_data:
        if vm[1]['dom_name'] == vm[1]['hypervisor']:
            max_memory = float(vm[1]['max_memory'])
        else:
            if vm[1]['state'] == "up":
                memory_up += float(vm[1]['max_memory'])
                disk_up   += float(vm[1]['volsize'])
            memory += float(vm[1]['max_memory'])
            disk   += vm[1]['volsize']

    # Transform Unit
    memory_up = memory_up / (1024 ** UNITS[args['unit']])
    max_memory = max_memory / (1024 ** UNITS[args['unit']])
    if args['unit'][-1] == 'b':
        memory_up = memory_up * 8
        max_memory = max_memory * 8
        

    prct_used = memory_up / max_memory * 100
    if prct_used > float(args['critical']):
        data = "CRITICAL - Too much unit used : %0.2f%% "\
               "| memory=%0.2f%s;%0.2f;%0.2f;0.0;%0.2f" % \
                (prct_used,
                 memory_up,
                 args['unit'],
                 max_memory * float(args['warning'] / 100),
                 max_memory * float(args['critical'] / 100),
                 max_memory)
    elif prct_used > float(args['warning']):
        data = "WARNING - Too much unit used : %0.2f%% "\
               "| memory=%0.2f%s;%0.2f;%0.2f;0.0;%0.2f" % \
                (prct_used,
                 memory_up,
                 args['unit'],
                 max_memory * float(args['warning'] / 100),
                 max_memory * float(args['critical'] / 100),
                 max_memory)
    else:
        data = "OK - Unit used : %0.2f%% "\
                "| memory=%0.2f%s;%0.2f;%0.2f;0.0;%0.2f" % \
                (prct_used,
                 memory_up,
                 args['unit'],
                 max_memory * float(args['warning'] / 100),
                 max_memory * float(args['critical'] / 100),
                 max_memory)

    # Print output
    print data

    # Exit with status code
    if memory_up > max_memory * float(args['critical'] / 100):
        sys.exit(STATE_CRITICAL)
    elif memory_up > max_memory * float(args['warning'] / 100):
        sys.exit(STATE_WARNING)
    else:
        sys.exit(STATE_OK)


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = [
                           'uri',
                           'unit',
                           'warning',
                           'critical',
                           ]
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument `%s' is missing !" % argument_name
            print_support()
            sys.exit(STATE_UNKNOWN)

    for t in ['warning', 'critical']:
        if args[t].endswith('%'):
            args[t] = args[t][:-1]
        try:
            args[t] = float(args[t])
        except:
            print "%s threshold : bad format !" % t.capitalize()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if args['warning'] > args['critical']:
        print "Warning threshold must be less than critical threshold"
        print_support()
        sys.exit(STATE_UNKNOWN)

    if not args['unit'] in UNITS.keys():
        print "Unit : bad format !"
        print_support()
        sys.exit(STATE_UNKNOWN)

    uri = urlparse(args['uri'])
    if not uri.scheme:
        print "URI : bad format !"
        print_support()
        sys.exit(STATE_UNKNOWN)
    
    if len(uri.scheme.split("+", 1)) == 2:
        ptcl, tp = uri.scheme.split("+", 1)
        if not ptcl in LIBVIRT_PROTOCOLS:
            print "URI : bad protocol !"
            print_support()
            sys.exit(STATE_UNKNOWN)
        if not tp in LIBVIRT_TRANSPORTS:
            print "URI : bad transport !"
            print_support()
            sys.exit(STATE_UNKNOWN)
    else:
        if not uri.scheme in LIBVIRT_PROTOCOLS:
            print "URI : bad protocol !"
            print_support()
            sys.exit(STATE_UNKNOWN)

def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'hVw:c:u:U:',
                        ['help', 'version',
                         'warning', 'critical', 'uri', 'unit'])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-u", "--uri"):
            args['uri'] = value
        elif option_name in ("-U", "--unit"):
            args['unit'] = str(value)
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
