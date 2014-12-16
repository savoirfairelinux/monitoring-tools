#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Browse web site to find broken links
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
#               check_site_health Browse web site to find broken links
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#

import getopt
import sys
import re
from subprocess import PIPE, Popen

PLUGIN_NAME = "check_site_health"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4

STATUS_CODES = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing (WebDAV; RFC 2518)',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information (since HTTP/1.1)',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi-Status (WebDAV; RFC 4918)',
    208: 'Already Reported (WebDAV; RFC 5842)',
    226: 'IM Used (RFC 3229)',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other (since HTTP/1.1)',
    304: 'Not Modified',
    305: 'Use Proxy (since HTTP/1.1)',
    306: 'Switch Proxy',
    307: 'Temporary Redirect (since HTTP/1.1)',
    308: 'Permanent Redirect (approved as experimental RFC)[12]',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: "I'm a teapot (RFC 2324)",
    420: 'Enhance Your Calm (Twitter)',
    422: 'Unprocessable Entity (WebDAV; RFC 4918)',
    423: 'Locked (WebDAV; RFC 4918)',
    424: 'Failed Dependency (WebDAV; RFC 4918)',
    424: 'Method Failure (WebDAV)[14]',
    425: 'Unordered Collection (Internet draft)',
    426: 'Upgrade Required (RFC 2817)',
    428: 'Precondition Required (RFC 6585)',
    429: 'Too Many Requests (RFC 6585)',
    431: 'Request Header Fields Too Large (RFC 6585)',
    444: 'No Response (Nginx)',
    449: 'Retry With (Microsoft)',
    450: 'Blocked by Windows Parental Controls (Microsoft)',
    451: 'Unavailable For Legal Reasons (Internet draft)',
    451: 'Redirect (Microsoft)',
    494: 'Request Header Too Large (Nginx)',
    495: 'Cert Error (Nginx)',
    496: 'No Cert (Nginx)',
    497: 'HTTP to HTTPS (Nginx)',
    499: 'Client Closed Request (Nginx)',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    506: 'Variant Also Negotiates (RFC 2295)',
    507: 'Insufficient Storage (WebDAV; RFC 4918)',
    508: 'Loop Detected (WebDAV; RFC 5842)',
    509: 'Bandwidth Limit Exceeded (Apache bw/limited extension)',
    510: 'Not Extended (RFC 2774)',
    511: 'Network Authentication Required (RFC 6585)',
    598: 'Network read timeout error (Unknown)',
    599: 'Network connect timeout error (Unknown)',
    'CODE_NOT_FOUND': 'HTTP Code not found',
}


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
%s.py -H <host> [-w <warning_codes> -c <critical_codes> | -o <ok_codes>]

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -V, --version
    Print version information
 -w, --warning=code list
    Http codes to define WARNING status
    example: -w 404,500,502,503,504
    default:
 -c, --critical=code list
    Http codes to define CRITICAL status
    example: -c 404,500,502,503,504
    default:
 -o, --ok=code list
    Http codes to define OK status, if all other codes define CRITICAL status
    exemple: -o 200,302
""" % PLUGIN_NAME
    print usage_msg


def get_data(args):
    """Fetch data
    """
    url = args['hostname']
    command = ["wget",
                "--random-wait",
                "-nd",
                "-rpe",
                "robots=off",
                '--delete-after',
                "-U",
                "mozilla",
                url,
                ]
    # Browse web site
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    err = "\n\n" + err
    output = err.split("\n\n--")[1:]
    result = {}
    # Search status code
    for page in output:
        lines = page.split('\n')
        uri = lines[0].split("--  ")[-1]
        status_code = 'CODE_NOT_FOUND'
        for line in lines:
            if line.startswith('HTTP request sent'):
                status_code = re.findall('(\d\d\d)', line)
                if len(status_code) == 1:
                    status_code = int(status_code[0])
                else:
                    status_code = 'CODE_NOT_FOUND'
            elif re.findall('failed: (.*)$', line):
                status_code = re.findall('failed: (.*)$', line)[0]

        if not status_code in result:
            result[status_code] = [uri]
        else:
            result[status_code].append(uri)

    # Prepare results
    messages = {}
    counters = {}
    for error in ['warning', 'critical', 'ok']:
        if error not in args:
            continue

        messages[error] = ''
        counters[error] = 0
        for error_code in args[error]:
            if error_code in result:
                for error_uri in result[error_code]:
                    counters[error] += 1
                    tmp = "%s: %s (%s)" % (error_uri, str(error_code),
                                           STATUS_CODES[error_code])
                    if messages[error]:
                        messages[error] = " - ".join((messages[error], tmp))
                    else:
                        messages[error] = tmp

    # Check if all fetched codes are in STATUS_CODE
    for error_code, pages in result.items():
        if not error_code in STATUS_CODES:
            for page in pages:
                counters['critical'] += 1
                tmp = "%s: CODE_NOT_FOUND (%s)" % (page, error_code)
                if messages['critical']:
                    messages['critical'] = " - ".join((messages['critical'],
                                                       tmp))
                else:
                    messages['critical'] = tmp

    # Prepare message
    perfdata = ""
    num_pages = sum([len(uri) for uri in result.values()])
    perfdata_num_pages = ' num_pages=%d;;;0;' % num_pages
    if 'ok' in args:
        if counters['ok'] == num_pages:
            msg = 'OK : no failed page found'
            exit_code = STATE_OK
        else:
            msg = ''
            for error_code, pages in result.items():
                if error_code in args['ok']:
                    continue
                for page in pages:
                    if not error_code in STATUS_CODES:
                        tmp = "%s: %s " % (page, str(error_code))
                    else:
                        tmp = "%s: %s (%s)" % (page,
                                               str(error_code),
                                               STATUS_CODES[error_code])

                    if msg:
                        msg = " - ".join((msg, tmp))
                    else:
                        msg = tmp
            msg = 'CRITICAL : ' + msg
            exit_code = STATE_CRITICAL

        critical_pages = num_pages - counters['ok']
        perfdata = ' num_critical_pages=%d;;;0;' % critical_pages
    else:
        if 'critical'in counters and counters['critical'] > 0:
            msg = 'CRITICAL : '
            msg = msg + messages['critical']
            perfdata_critical_pages = ' num_critical_pages=%d;;;0;' \
                                       % counters['critical']
            perfdata = perfdata + perfdata_critical_pages
            exit_code = STATE_CRITICAL
            if 'warning' in messages:
                msg = msg + " - " + messages['warning']
        elif 'warning' in counters and counters['warning'] > 0:
            msg = 'WARNING : '
            msg = msg + messages['warning']
            perfdata_warning_pages = ' num_warning_pages=%d;;;0;' \
                                      % counters['warning']
            perfdata = perfdata + perfdata_warning_pages
            exit_code = STATE_WARNING
        else:
            msg = 'OK - no failed page found'
            exit_code = STATE_OK
    perfdata = perfdata + perfdata_num_pages

    # Prepare perfdata
    print msg + " |" + perfdata

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

    if not args['hostname'].startswith("http://") \
    and not args['hostname'].startswith("https://"):
        args['hostname'] = "http://" + args['hostname']

    if 'ok' in args:
        if 'critical' in args or 'warning' in args:
            print 'You can define OK option and WARNING/CRITICAL options'
            print_usage()
            print_support()
            sys.exit(STATE_UNKNOWN)
        else:
            try:
                args['ok'] = [int(code) for code in args['ok'].split(",")]
            except:
                print "Bad format for OK argument"
                print_usage()
                print_support()
                sys.exit(STATE_UNKNOWN)
    else:
        if not ('warning' in args or 'critical' in args):
            args['critical'] = [404, 500, 502, 503, 504]

        else:
            if 'warning' in args:
                try:
                    args['warning'] = [int(code)
                                       for code in args['warning'].split(",")]
                except:
                    print "Bad format for WARNING argument"
                    print_usage()
                    print_support()
                    sys.exit(STATE_UNKNOWN)

            if 'critical' in args:
                try:
                    args['critical'] = [int(code)
                                       for code in args['critical'].split(",")]
                except:
                    print "Bad format for CRITICAL argument"
                    print_usage()
                    print_support()
                    sys.exit(STATE_UNKNOWN)

    if 'critical' in args:
        args['critical'].append('CODE_NOT_FOUND')
    else:
        args['critical'] = ['CODE_NOT_FOUND']

    return args


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:hVw:c:o:',
                        ['hostname=', 'help', 'version', 'ok=',
                         'warning=', 'critical='])
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
        elif option_name in ("-o", "--ok"):
            args['ok'] = value
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
