#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check various things from a rancid repo depending on the mode.
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
#               check_rancid Check various things from a rancid repo depending on the mode.
#
#
#     Author: Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#

import getopt
import sys
import os
import datetime
import re
import pysvn
import urllib
import time
import syslog

PLUGIN_NAME = "check_rancid"
PLUGIN_VERSION = "0.1"
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
STATE_DEPENDENT = 4
MANDATORY_ARGS_MOD = {
    'ping': ['hostname', 'path'],
    'hash': ['path'],
    'cards': ['path'],
    'config': ['path'],
    'qos': ['path'],
    'filter': ['path'],

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
%s.py -H <host or group> -P <path> -M <mode>

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=STRING
    Host name or group of hosts
 -V, --version
    Print version information
 -P, --path=STRING
    Path to rancid var directory. Usually the dir contains a logs dirs and hostgroup dirs
    Example : /usr/local/rancid/var
 -M, --mod=STRING
    Plugin mod. Must be one of the following : ping, hash, config, cards, filter, qos
      *ping:
        Check if all host in the hostgroup are up from the rancid point of view.
        It uses the .up file to determine the lists of host to look for
      *hash:
        Check if the firmware hash is different from the ref one (or from the previous one)
      *config:
        Check if the configuration has changed for the host / group (notify diff)
      *cards:
        Specific to 8600 models. Check the hardware cards plugged to the host (notify diff).
      *filter:
        Specific to ES-470. Check the filters (notify diff)
      *qos:
        Specific to ES-470. Check the qos values (notify diff)
 -u, --url=URL
    URL to submit passive results to Shinken Receiver with HTTP
    Need a host and service to send result.
 -a, --passive-host=STRING
    Required if not in plugin mod to send data to Shinken ws_arbiter
 -b, --passive-service=STRING
    Required if not in plugin mod to send data to Shinken ws_arbiter
""" % PLUGIN_NAME
    print usage_msg


# Try to send data with urllib through the url
# Return 0 if success, 1 else
def send_data(url, data):
    try:
        answer = urllib.urlopen(url, data)
        if 200 <= answer.code < 300:
            return 0
        else:
            raise Exception("Error sending data to %s. Error code : %s" % (url, answer.code))
    except IOError:
        raise Exception("Cannot connect to %s. Data was not sent" % url)


def do_exit(output, code, mod_plugin=True,  url=None, host=None, svc=None):

    if mod_plugin:
        print output
        sys.exit(code)

    else:
        time_stamp = int(time.time())
        data = "host_name=%s&service_description=%s&return_code=%d&output=%s&time_stamp=%s&" % \
            (host, svc, code, output, time_stamp)

        try:
            send_data(url, data)
        except Exception as e:
            msg = str(e)
            syslog.syslog(syslog.LOG_USER | syslog.LOG_ERR, msg)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def get_data_ping(args):
    """Fetch data for mod
    """
    if not 'group_dir' in args.keys():
        do_exit("UNKNOWN : The --hostname option for ping mod should be a group of hosts!", STATE_UNKNOWN)

    if not 'log_dir' in args.keys():
        do_exit("UNKNOWN : No logs directory found in %s!" % args['path'], STATE_UNKNOWN)

    host_num = file_len(os.path.join(args['group_dir'], 'routers.up'))

    files = [file for file in os.listdir(args['log_dir']) if file.startswith(args['hostname'])]
    files = sorted(files, key=lambda x: int(x.split('.')[1]+x.split('.')[2]))

    last_update = datetime.datetime.strptime(files[0], args['hostname'] + '.%Y%m%d.%H%M%S')
    # Check if it older than 6 hours old
    if last_update - datetime.datetime.now() > datetime.timedelta(0, 21600):
        do_exit("UNKNOWN : The log file is too old", STATE_CRITICAL,
                args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])

    host_missing = []
    last_round = 0
    for _, l in enumerate(open(os.path.join(args['log_dir'], files[0]))):
        if re.search("All routers sucessfully completed", l) is not None:
            do_exit("OK : Everything is up | %.3f;%.3f;0;;" % (host_num, host_num - 1), STATE_OK,
                    args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])
        matches = re.search("(.*): End of run not found", l)
        if matches is not None:
            host_missing.append(matches.groups()[0])
        matches = re.search("Getting missed routers: round ([0-9]+)\.", l)
        if matches is not None:
            last_round = matches.groups()[0]
            host_missing = []

    if len(host_missing) == 0:
        do_exit("UNKNOWN : There is no error detected but there is no line mentioning everything is OK.", STATE_UNKNOWN,
                args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])

    if len(host_missing) == host_num:
        do_exit("CRITICAL : All host down after %s rounds! | %.3f;%.3f;0;;" % (last_round, host_num, host_num - 1),
                STATE_WARNING, args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])
    else:
        do_exit("WARNING : One or more host down after %s rounds | %.3f;%.3f;0;;" % (last_round, len(host_missing), host_num - 1),
                STATE_CRITICAL, args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])


def get_data_hash(args):
    """Fetch data for mod
    """
    pass


def get_data_cards(args):
    """Fetch data for mod
    """
    diff_data(args, "Slot  ([0-9])")


def get_data_config(args):
    """Fetch data for mod
    """
    diff_data(args, ".")


def get_data_qos(args):
    """Fetch data for mod
    """
    diff_data(args, "qos")


def get_data_filter(args):
    """Fetch data for mod
    """
    diff_data(args, "filter")


def diff_data(args, pattern):
    if not 'group_dir' in args.keys():
        do_exit("UNKNOWN : The --hostname group for %s mod is not found" % args['mod'], STATE_UNKNOWN)

    cli = pysvn.Client()
    new_rev = cli.update(args['group_dir'])[0]
    old_file = os.path.join("/tmp/", args['hostname'], args['mod'])
    if os.path.exists(old_file):
        fil = open(old_file)
        old_rev_num = fil.read()
        fil = open(old_file, "w")
        file.write(new_rev.number)
        fil.close()

    else:
        old_rev_num = new_rev.number - 1
    diff = cli.diff("/tmp", args['group_dir'], new_rev,
                    args['group_dir'], pysvn.Revision(pysvn.opt_revision_kind.number, old_rev_num))

    matches = re.search(pattern, diff)

    if matches is None:
        do_exit("OK : Configuration remains unchanged for %s" % args['hostname'], STATE_OK,
                args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])
    else:
        do_exit("WARNING : Configuration has changed for %s" % args['hostname'], STATE_WARNING,
                args['mod-plugin'], args['url'], args['passive-hostname'],  args['passive-service'])


def check_arguments(args):
    """Check mandatory fields
    """
    if 'mod' in args.keys():
        if args['mod'] in MANDATORY_ARGS_MOD.keys():
            mandatory_arguments = MANDATORY_ARGS_MOD[args['mod']]
        else:
            print_usage()
            print_support()
            do_exit("UNKNOWN : Mod '%s' unknown!" % args['mod'], STATE_UNKNOWN)
    else:
        mandatory_arguments = ['mod']

    for argument_name in mandatory_arguments:
        if not argument_name in args.keys():
            print_usage()
            print_support()
            do_exit("UNKNOWN : Argument '%s' is missing !" % argument_name, STATE_UNKNOWN)

    if os.path.isdir(os.path.join(args['path'], "logs")):
        args['log_dir'] = os.path.join(args['path'], "logs")

    if os.path.isdir(os.path.join(args['path'], args['hostname'])):
        args['group_dir'] = os.path.join(args['path'], args['hostname'])

    if 'mod-plugin' in args.keys() == ('url' in args.keys() and
                                       'passive-host' in args.keys() and
                                       'passive-service' in args.keys()):
        do_exit("UNKNOWN : Please specify mod-plugin or (url and host and service)", STATE_UNKNOWN)

    if 'mod-plugin' not in args.keys():
        args['mod-plugin'] = False




def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:P:M:hVu:a:b:p',
                        ['hostname=', 'path=', 'mod=', 'help', 'version',
                         'url=', 'passive-host=', 'passive-service', 'mod-plugin']
        )
    except getopt.GetoptError, err:
        print_usage()
        do_exit(STATE_UNKNOWN, str(err))

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        elif option_name in ("-P", "--path"):
            args['path'] = value
        elif option_name in ("-M", "--mod"):
            args['mod'] = value
        elif option_name in ("-u", "--url"):
            args['url'] = value
        elif option_name in ("-a", "--passive-host"):
            args['passive-host'] = value
        elif option_name in ("-b", "--passive-service"):
            args['passive-service'] = value
        elif option_name in ("-p", "--mod-plugin"):
            args['mod-plugin'] = True
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

    f = globals()['get_data_'+args['mod']]
    f(args)


if __name__ == "__main__":
    main()
