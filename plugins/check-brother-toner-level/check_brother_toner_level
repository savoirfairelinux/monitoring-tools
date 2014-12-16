#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check toner levels of Brother printer by http
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
#               check_brother_toner_level Check toner levels of Brother printer by http
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
from StringIO import StringIO
import re

import requests
from lxml import etree


PLUGIN_NAME = "check_brother_toner_level"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4
TIMEOUT = 15


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
%s.py -H <host> [-w <warning> -c <critical>] [-n <name>] [-s]

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -V, --version
    Print version information
 -w, --warning=DOUBLE
    Warning percent level. Default: 20
 -c, --critical=DOUBLE
    critical percent level. Default: 5
 -s, --show-all
    Show all consumables even if there are OK
 -n, --consumable
    Reg Exp of consumable name. Default: empty (match all)
""" % PLUGIN_NAME
    print usage_msg


def get_level(raw_level):
    raw_level = raw_level.strip()
    current_level = raw_level.count(u'\u25a0')
    empty_level = raw_level.count(u'\u25a1')
    level_max = float(current_level + empty_level)
    if level_max == 0:
        return None
    level = current_level * 100 / level_max
    return level


def get_data(args):
    """Fetch data
    """
    results = {}
    results = get_mnt_info(args, results)
    results = get_view_config(args, results)

    if 'consumable' in args:
        for k in results.keys():
            if not re.search(args['consumable'], k):
                del(results[k])

    msg = ''
    perfdata = ''
    exit_code = STATE_OK
    for name, value in results.items():
        tmp_dict = {
                    'name': name,
                    'value': value,
                    'critical': args['critical'],
                    'warning': args['warning'],
                    }

        perfdata = perfdata + " %(name)s=%(value)0.2f%%;%(warning)0.2f;%(critical)0.2f;0;100;" % tmp_dict

        if value <= args['critical']:
            exit_code = STATE_CRITICAL
            if not msg:
                msg = "CRITICAL: %(name)s: %(value)0.2f%%" % tmp_dict
            else:
                msg = msg + " -- CRITICAL: %(name)s: %(value)0.2f%%" % tmp_dict
        elif value <= args['warning'] and exit_code < STATE_CRITICAL:
            exit_code = STATE_WARNING
            if not msg:
                msg = "WARNING: %(name)s: %(value)0.2f%%" % tmp_dict
            else:
                msg = msg + " -- WARNING: %(name)s: %(value)0.2f%%" % tmp_dict
        else:
            if args['show']:
                if not msg:
                    msg = "%(name)s: %(value)0.2f%%" % tmp_dict
                else:
                    msg = msg + " -- %(name)s: %(value)0.2f%%" % tmp_dict

    if msg == '':
        msg = "All consumables are OK"

    exit_string = msg + " |" + perfdata

    if len(results) == 0:
        exit_string = "No consumables found..."
        exit_code = STATE_UNKNOWN

    print exit_string
    sys.exit(exit_code)


def get_mnt_info(args, results):
    url = "http://" + args['hostname'] + "/etc/mnt_info.html"
    try:
        res = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.Timeout, e:
        print "HTTP request timeout"
        sys.exit(STATE_UNKNOWN)
    except Exception, e:
        print str(e)
        return results

    if res.status_code == 404:
        return results

    parser = etree.HTMLParser()
    html = etree.parse(StringIO(res.content), parser)
    for i, cell in enumerate(html.findall('//tr/td/dd')):
        # Get Toner level
        if re.search('Toner', cell.text):
            consumable_name = cell.text.strip()
            consumable_name = consumable_name.replace("*", "")
            raw_level_el = cell.getparent().getparent().find('./td[@class="elem"]')
            level = get_level(raw_level_el.text)
            if not level is None:
                results[consumable_name] = level
        # Get Other consumable level
        elif re.search('(% of Life Remaining)', cell.text):
            raw_level = cell.getparent().getparent().find('./td[@class="elem"]').text
            row = cell.getparent().getparent()
            table = row.getparent()
            consumable_name = table.getchildren()[i+2].getchildren()[0].getchildren()[0].text
            consumable_name = consumable_name.strip()
            consumable_name = consumable_name.replace("*", "")
            if not consumable_name:
                continue
            level = re.search('\d\d\.\d\d|\d\d', raw_level)
            if not level is None:
                results[consumable_name] = float(level.group())

    return results


def get_view_config(args, results):
    url = "http://" + args['hostname'] + "/etc/view_config.html"
    try:
        res = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.Timeout, e:
        print "HTTP request timeout"
        sys.exit(STATE_UNKNOWN)
    except:
        return results


    if res.status_code == 404:
        return results

    parser = etree.HTMLParser()
    html = etree.parse(StringIO(res.content), parser)
    for i, cell in enumerate(html.findall('//tr/td[@class="elem"]')):
        # Get Toner level
        text = " - ".join([t.strip() for t in cell.itertext()])
        if text.find(u'\u25a0') != -1 and text.find(u'\u25a1') != -1:
            consumable_el = cell.getparent().find('./td[@class="TagLPurprB"]')
            consumable_name = consumable_el.text.strip()
            consumable_name = "Toner " + consumable_name
            level = get_level(text)
            if not consumable_name:
                continue
            if not level is None:
                results[consumable_name] = level

    return results


def check_arguments(args):
    """Check mandatory fields
    """
    mandatory_arguments = ['hostname'
                           ]
    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print "Argument `%s' is missing !" % argument_name
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)

    if not 'warning' in args.keys():
        args['warning'] = 20.00
    else:
        args['warning'] = float(args['warning'])

    if not 'critical' in args.keys():
        args['critical'] = 5.00
    else:
        args['critical'] = float(args['critical'])

    if args['warning'] < args['critical']:
        print "Warning threshold must be greater than Critical threshold"
        print_support()
        sys.exit(STATE_UNKNOWN)

    if not 'show' in args.keys():
        args['show'] = False


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:hVsw:c:n:',
                        ['hostname=', 'consumable=',
                         'help', 'version', 'show-all',
                         'warning', 'critical'])
    except getopt.GetoptError, err:
        print str(err)
        print_usage()
        sys.exit(STATE_UNKNOWN)

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        elif option_name in ("-w", "--warning"):
            args['warning'] = value
        elif option_name in ("-c", "--critical"):
            args['critical'] = value
        elif option_name in ("-n", "--consumable"):
            args['consumable'] = value
        elif option_name in ("-s", "--show-all"):
            args['show'] = True
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
