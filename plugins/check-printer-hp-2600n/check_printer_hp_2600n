#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check HP Color LaserJet 2600n status
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
#               check_printer_hp_2600n.py Check HP Color LaserJet 2600n status
#
#
#     Author: Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import getopt
import sys

PLUGIN_NAME = "check_printer_hp_2600n"
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
    Page to get with http. Default /SSI/device_status_info.htm
 -w, --warning=FLOAT
    warning thresold
 -c, --critical=FLOAT
    critical thresold
 -C, --color=STRING
    filter only on the specified color
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
    # The findall look for everty td tag into the html code
    # We want the node where the td width is 25%
    # Then we keep only the name (COLOR CARTRIDGE) and the percent associated
    # In this case there are 4 couples: one for each color
    color_list = \
        dict([(x.text.split(u" ")[0], x.text.split(u"\xa0")[-1].replace('%', ''))
             for x in html.findall("//table//td[@width='25%']/font")])

    if color_list == {}:
        print "CRITICAL - Can't get data from the device"
        sys.exit(STATE_CRITICAL)

    if "color" in args and args['color'] not in color_list:
        print "UNKNOWN - Color %s not in found data collected" % args['color']
        sys.exit(STATE_UNKNOWN)
    elif "color" in args:
        #subdict = {x: y for x, y in color_list.items() if x == args['color']}
        subdict = dict([(x, y) for x, y in color_list.items() if x == args['color']])
        output, code = gen_output(subdict, args['warning'], args['critical'])
    else:
        output, code = gen_output(color_list, args['warning'], args['critical'])
    print output
    sys.exit(code)


def gen_output(color_list, warning, critical):
    perfdata = ""
    output = {'critical': [], 'warning': []}
    for color, percent in color_list.items():
        if critical < int(percent) <= warning:
            output['warning'].append(" %s (%0.3f,%0.3f)" % (color, float(percent), warning))
        elif  int(percent) <= critical:
            output['critical'].append(" %s (%0.3f,%0.3f)" % (color, float(percent), critical))
        perfdata += "%s=%0.1f%%;%0.1f;%0.3f;0.0;100.0 " % (color, float(percent), warning, critical)

    if len(output['critical']) > 0:
        concat_ouput = "CRITICAL #" + " " .join(output['critical']) + "|" + perfdata
        code = STATE_CRITICAL
    elif len(output['warning']) > 0:
        concat_ouput = "WARNING #" + " ".join(output['warning']) + "|" + perfdata
        code = STATE_WARNING
    else:
        concat_ouput = "OK # Toners OK" + "|" + perfdata
        code = STATE_OK

    return concat_ouput, code


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['hostname', 'warning', 'critical']
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "UNKNOWN - Argument '%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'port' in args.keys():
        args['port'] = '80'

    if not 'page' in args.keys():
        args['page'] = '/SSI/device_status_info.htm'

    if args['warning'] < args['critical']:
        print "UNKNOWN - Wrong warning or critical values."\
              " Please ensure warning > critical"
        sys.exit(STATE_UNKNOWN)


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            'H:hVP:p:w:c:C:',
            ['hostname=', 'help', 'version', 'port=', 'page='])

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
        elif option_name in ("-c", "--critical"):
            args['critical'] = float(value)
        elif option_name in ("-w", "--warning"):
            args['warning'] = float(value)
        elif option_name in ("-C", "--color"):
            args['color'] = value.upper()
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
