#!/usr/bin/python
# -*- coding: utf-8 -*-
"""A Nagios plug-in to use OpenStack Ceilometer API for metering
"""
#
#
#     Copyright (C) 2014 Savoir-Faire Linux Inc.
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
#               check_ceilometer
#       A Nagios plug-in to use OpenStack Ceilometer API for metering
#
#
#     Author: Alexandre Viau <alexandre.viau@savoirfairelinux.com>
#
#

import getopt
import sys

PLUGIN_NAME = "check_ceilometer"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3


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
Send email to <alexandre.viau@savoirfairelinux.com> if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to <alexandre.viau@savoirfairelinux.com>
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
"""
    print support_msg


def print_usage():
    """Show how to use this plugin
    """
    usage_msg = """
%s.py  -r <resource id> -m <meter>  -w <warning> -c <critical> \
-u <os_username> -p <os_password> -t <os_tenant_name> -a <os_auth_url>

Usage:
 -h, --help
    Print detailed help screen
 -V, --version
    Print version information
 -r --resource_id=STRING
    Resource id of the meter
 -m --meter_name=STRING
    Name of the meter
 -w, --warning=DOUBLE
    Value to result in warning status (seconds)
 -c, --critical=DOUBLE
    Value to result in critical status (seconds)
 -u os_username=STRING
    Your user name
 -p os_password=STRING
    Your password
 -t os_tenant_name=STRING
    Your tenant name
 -a os_auth_url
    Ceilometer endpoint
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    from ceilometerclient import client as ceil_client
    import json

    try:
        ceilometer = ceil_client.get_client(
            '2',
            os_username=args['os_username'],
            os_password=args['os_password'],
            os_tenant_name=args['os_tenant_name'],
            os_auth_url=args['os_auth_url']
        )
    except Exception, e:
        print e.message
        sys.exit(STATE_UNKNOWN)

    filters = {
        "and": [
            {"=": {"resource_id": args['resource_id']}},
            {"=": {"meter": args['meter_name']}}
        ]
    }
    order_by = [{"timestamp": "DESC"}]

    try:
        samples = ceilometer.query_samples.query(json.dumps(filters),
                                                 json.dumps(order_by),
                                                 1)
    except Exception, e:
        print e.message
        sys.exit(STATE_UNKNOWN)

    if len(samples) > 0:
        sample = samples[0]
    else:
        print "No samples"
        sys.exit(STATE_UNKNOWN)

    output = ("%(meter)s on %(resource_id)s is: "
              "%(volume)0.2f %(unit)s" % sample.__dict__)
    perf_data = "%(meter)s=%(volume)0.2f%(unit)s" % sample.__dict__ + \
                ";%s;%s;;" % (args['warning'], args['critical'])

    if sample.volume >= args['critical']:
        print 'CRITICAL - %s | %s' % (output, perf_data)
        sys.exit(STATE_CRITICAL)
    elif sample.volume >= args['warning']:
        print 'WARNING - %s | %s' % (output, perf_data)
        sys.exit(STATE_WARNING)
    else:
        print 'OK - %s | %s' % (output, perf_data)
        sys.exit(STATE_OK)


def check_arguments(args):
    """Check mandatory fields
    """
    import os

    os_arguments = ['os_username',
                    'os_password',
                    'os_tenant_name',
                    'os_auth_url']

    for argument_name in os_arguments:
        if argument_name not in args.keys() and argument_name in os.environ:
            args[argument_name] = os.environ[argument_name]

    mandatory_arguments = ['resource_id',
                           'meter_name',
                           'warning',
                           'critical',
                           'os_username',
                           'os_password',
                           'os_tenant_name',
                           'os_auth_url']

    for argument_name in mandatory_arguments:
        if argument_name not in args.keys():
            print "Argument '%s' is missing!" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    float_arguments = ['warning', 'critical']

    for argument_name in float_arguments:
        try:
            args[argument_name] = float(args[argument_name])
        except ValueError:
            print "Argument '%s': not float!" % argument_name
            sys.exit(STATE_UNKNOWN)


def main():
    """Main function
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      'hVr:m:w:c:u:p:t:a:',
                                      ['help',
                                       'version',
                                       'resource_id=',
                                       'meter_name=',
                                       'warning=',
                                       'critical=',
                                       'os_username=',
                                       'os_password=',
                                       'os_tenant_name=',
                                       'os_auth_url='])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-r", "--resource_id"):
            args['resource_id'] = value
        elif option_name in ("-m", "--meter_name"):
            args['meter_name'] = value
        elif option_name in ("-w", "--warning"):
            args['warning'] = value
        elif option_name in ("-c", "--critical"):
            args['critical'] = value
        elif option_name in ("-u", "--os_username"):
            args['os_username'] = value
        elif option_name in ("-p", "--os_password"):
            args['os_password'] = value
        elif option_name in ("-t", "--os_tenant_name"):
            args['os_tenant_name'] = value
        elif option_name in ("-a", "--os_auth_url"):
            args['os_auth_url'] = value
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
