#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2014, vdnguyen <vanduc.nguyen@savoirfairelinux.com>

import os
import os.path
import time
import datetime
import argparse
import warnings

from shinkenplugins.perfdata import PerfData
from shinkenplugins.helpers.argparse import escape_help
from shinkenplugins.helpers.argparse.parsing.bytes import (
    ByteAmountParser,
    adv_byte_unit_to_transformer,
    PercentValue,
)
from shinkenplugins.plugin import ShinkenPlugin

#############################################################################

unit_to_transformer = adv_byte_unit_to_transformer.copy()
unit_to_transformer[''] = lambda value: value * 2**30  # no unit -> GB

parse_bandwidth = ByteAmountParser('byte or percent', unit_transformers=unit_to_transformer)

class BandwidthThresholdAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value = parse_bandwidth(values)
        setattr(namespace, self.dest, value)

limit_transformer = unit_to_transformer.copy()
limit_transformer.pop('%')
parse_limit = ByteAmountParser('byte', unit_transformers=limit_transformer)


class PercentBandwidthThresholdAction(BandwidthThresholdAction):
    def __call__(self, parser, namespace, values, option_string=None):
        warnings.warn('%s is deprecated argument, please use either --warning or --critical' % option_string)
        super(PercentBandwidthThresholdAction, self).__call__(
            parser, namespace, values+'%', option_string=option_string)


#############################################################################

def make_interface_name(value):
    with open('/proc/net/dev', 'r') as fh:
        dev = fh.readlines()
    interface_dict = {}
    for line in dev[2:]:
        intf = line[:line.index(":")].strip()
        interface_dict[intf] = [int(v) for v in line[line.index(":") + 1:].split()]
    try:
        interface_dict[value]
    except KeyError:
        msg = ("There is not an intrface named: %r\n"
               "Interfaces unavailable: :"
               "%s" % (value, ", ".join(interface_dict.keys()))
              )
        raise ValueError(msg)
    return value

#############################################################################

class CheckLinuxBandwidth(ShinkenPlugin):
    NAME = 'check-linux-bandwidth-usage'
    VERSION = '0.1'
    DESCRIPTION = 'check linux bandwidth usage per month'
    AUTHOR = 'vdnguyen'
    EMAIL = 'vanduc.nguyen@savoirfairelinux.com'

    _warning_kwargs = {
        # to be able to correctly handle '-W' argument (see below)
        #'required': True,
        'action':   BandwidthThresholdAction,
        'help':     escape_help(
            'Limit to result in a warning state: <amount><unit>\n'
            'One can use many unit: TB|GB|MB|KB|% ; their meaning is self explanatory. unit if unset is GB.\n'
            'The prepended amount can be a float or an int. Examples:'
            '\t-w 30MB\n'
            '\t-w 0.5GB\n'
            '\t-w 10% --limit 30GB\n'
            'If you use % then you must also give the limit argument, which defines the maximal bandwidth for the given period.'
        )
    }
    _critical_kwargs = {
        # to be able to correctly handle '-C' argument (see below)
        #'required': True,
        'action':   BandwidthThresholdAction,
        'help':     escape_help(
            'Limit to result in a critical state: <amount><unit>\n'
            'One can use many unit: TB|GB|MB|KB|% ; their meaning is self explanatory. unit if unset is GB.\n'
            'The prepended amount can be a float or an int. Examples:'
            '\t-c 1.5GB\n'
            '\t-c 10% --limit 30GB\n'
            '\t..'
            'If you use % then you must also give the limit argument, which defines the maximal bandwidth for the given period.'
        )
    }

    #############################################################################

    def __init__(self):
        super(CheckLinuxBandwidth, self).__init__()
        add = self.parser.add_argument
        add('-i', '--interface-name', required=True, type=make_interface_name,
            help='The name of interface you want to have a bandwidth check.')
        self.add_warning_critical()
        add('-l', '--limit', type=parse_limit,
            help=escape_help('Mandatory if you use a % in warning or critical thresholds.\n'
                 '\tLimit of bandwidth per month: You can also use many unit: TB|GB|MB|KB ; if none provided -> GB.')),
        add('-d', '--reset-day', help='number of day to reset the counter', type=int),
        add('-s', '--cache-folder', default='/tmp/check_linux_bandwidth/',
            help='the folder to stock the data.'),
        add('-f', '--perfdata', action='store_true',
            help='option to show perfdata'),
        # so to be still compat with before:
        # TODO: deprecated, remove me in some time:
        add('-W', '--warning-percent', dest='warning', action=PercentBandwidthThresholdAction,
            help='For compatibility, please use --warning instead.')
        add('-C', '--critical-percent', dest='critical', action=PercentBandwidthThresholdAction,
            help='For compatibility, please use --critical instead.')

    def parse_args(self, args):
        args = super(CheckLinuxBandwidth, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required')
        if (isinstance(args.warning, PercentValue) or isinstance(args.critical, PercentValue)) and args.limit is None:
            self.parser.error('--limit is required if you supply a percent value for --warning or --critical')
        return args

    #############################################################################

    @staticmethod
    def file_accessible(filepath, mode):
        try:
            with open(filepath, mode):
                pass
        except IOError:
            return False
        return True

    @staticmethod
    def get_interfaces_datas():
        dev = open("/proc/net/dev", "r").readlines()
        interface_dict = {}
        for line in dev[2:]:
            intf = line[:line.index(":")].strip()
            interface_dict[intf] = [int(value) for value in line[line.index(":") + 1:].split()]
        return interface_dict

    @classmethod
    def get_total(cls, interface):
        """ Get interface total bandwidth
        """
        interface_dict = cls.get_interfaces_datas()
        receive = interface_dict[interface][0]
        transmit = interface_dict[interface][8]
        used_total = (float(receive) + float(transmit)) / (1024.0 ** 3)
        return used_total

    @classmethod
    def get_receive(cls, interface):
        # Get received data
        interface_dict = cls.get_interfaces_datas()
        receive = interface_dict[interface][0]
        receive = (float(receive)) / (1024.0 ** 3)
        return receive

    @classmethod
    def get_transmit(cls, interface):
        # Get transmit data
        interface_dict = cls.get_interfaces_datas()
        transmit = interface_dict[interface][8]
        transmit = (float(transmit)) / (1024.0 ** 3)
        return transmit

    @staticmethod
    def get_reset_day(reset_day):
        """ Find the data of next reset day """
        today = datetime.datetime.today()
        if reset_day > today.day:
            # If reset day 05 and today: 11 03 14 (m, d, y)
            reset_date = datetime.datetime(today.year, today.month, reset_day)
            # reset date: 11 05 14 (m, d, y)
        elif reset_day == today.day:
            # If reset day 03 and today: 11 03 14 (m, d, y)
            reset_date = datetime.datetime.today()
            # reset date: 11 03 14 (m, d, y)
        else:
            # If reset day 01 and today: 11 03 14 (m, d, y)
            if today.month == 12:
                # Handle december to january
                reset_date = today.replace(month=1, year=today.year + 1)
            else:
                # Handle next month
                reset_date = today.replace(month=today.month + 1)
            # reset date: 12 03 14 (m, d, y)
        return reset_date.strftime("%m%d%Y")

    def run(self, args):
        """ Main Plugin function """
        # Define variables
        ## perfdata
        p1 = ""
        p2 = ""
        p3 = ""
        p4 = ""
        ## total
        usage_per_month = 0.0
        used_total_percent = 0.0
        receive_per_month = 0.0
        transmit_per_month = 0.0

        ## output
        msg = ""
        # Get reset day
        day = args.reset_day
        # Get interface name
        interface = args.interface_name
        # Prepare interface variables

        # create cache_file with the name of interface and the path
        cache_file = os.path.join(args.cache_folder, interface + ".txt")

        interface_total = interface + "_total"
        interface_percent = interface + "_percent"
        interface_received = interface + "_received"
        interface_transmitted = interface + "_transmitted"

        # Get thresholds
        one_gb = 1024*1024*1024
        warning = args.warning
        critical = args.critical
        if not isinstance(warning, PercentValue):
            warning /= one_gb
        if not isinstance(critical, PercentValue):
            critical /= one_gb

        # Get limit
        limit = args.limit / one_gb if args.limit is not None else None

        # check if cache_folder exist if not create one
        if not os.path.exists(args.cache_folder):
            os.makedirs(args.cache_folder)


        # Get total
        new_total = self.get_total(interface)

        # Get received
        new_received = self.get_receive(interface)

        # Get transmit
        new_transmit = self.get_transmit(interface)

        # if the file doesn't exist
        if not os.path.isfile(cache_file):
            try:
                int_fh = open(cache_file, "w")
            except IOError:
                self.unknown("Cannot write temp file: %s" % cache_file)

            old_update = "00000000"

            # Write datas in file

            int_fh.write("%s %0.30f %0.30f %0.30f %0.30f "
                         "%0.30f %0.30f %0.30f %0.30f %0.30f" % (old_update,
                                                                 new_total,
                                                                 new_total,
                                                                 new_received,
                                                                 new_received,
                                                                 new_transmit,
                                                                 new_transmit,
                                                                 new_total,
                                                                 new_received,
                                                                 new_transmit))
            # Close file
            int_fh.close()

            # Exit for the first launch
            self.ok("First use of plugin")

        else:
            try:
                int_fh = open(cache_file, "r+")
            except IOError:
                self.unknown("Cannot read/write temp file: %s" % cache_file)
            # read file
            data_list = int_fh.readline()
            # prepare read datas
            data_list = data_list.strip().split()

            # get data
            old_update = data_list[0]

            # get totals
            prev_used_total = float(data_list[1])
            prev_receive_total = float(data_list[3])
            prev_transmit_total = float(data_list[5])

            # Get offsetsl
            prev_offset = float(data_list[2])
            prev_receive_offset = float(data_list[4])
            prev_transmit_offset = float(data_list[6])
            # get old datas

            old_data = float(data_list[7])
            old_receive = float(data_list[8])
            old_transmit = float(data_list[9])

            # get reset date
            reset_date = self.get_reset_day(day)
            # Get today
            to_day = time.strftime("%m%d%Y")
            # Check if the counter restarted

            if new_total >= prev_used_total:
                used_total = new_total
                receive_total = new_received
                transmit_total = new_transmit
            else:
                # Handle counter restart
                if new_total >= old_data:
                    used_total = prev_used_total + (new_total - old_data)
                    receive_total = prev_receive_total + (new_received - old_receive)
                    transmit_total = prev_transmit_total + (new_transmit - old_transmit)
                else:
                    used_total = prev_used_total + new_total
                    receive_total = prev_receive_total + new_received
                    transmit_total = prev_transmit_total + new_transmit

            # get all data to update storage file
            old_data = new_total
            old_receive = new_received
            old_transmit = new_transmit
            # get all data for output
            usage_per_month = used_total - prev_offset
            receive_per_month = receive_total - prev_receive_offset
            transmit_per_month = transmit_total - prev_transmit_offset
            # check if to day is reset date
            if to_day == reset_date and to_day != old_update:
                prev_offset = used_total
                prev_receive_offset = receive_total
                prev_transmit_offset = transmit_total
                old_update = reset_date
            # write data to file
            int_fh.seek(0)
            int_fh.write("%s %0.30f %0.30f %0.30f %0.30f "
                         "%0.30f %0.30f %0.30f %0.30f %0.30f" % (old_update,
                                                                 used_total,
                                                                 prev_offset,
                                                                 receive_total,
                                                                 prev_receive_offset,
                                                                 transmit_total,
                                                                 prev_transmit_offset,
                                                                 old_data,
                                                                 old_receive,
                                                                 old_transmit))
            int_fh.close()

        # check_linux_bandwidth_usage -i eth0 -W 50 -C 90 -d 10 -l 500
        if limit is not None and isinstance(warning, PercentValue):

            # calculate bandwidth per month in %
            usage_per_month_percent = (usage_per_month / limit) * 100
            # user does not give warning in GB so we have to calculate it
            s_warning = "%0.2f" % ((warning / 100) * limit)
            s_critical = "%0.2f" % ((warning / 100) * limit)
            # convert all data to float with 2 decimal places
            receive_per_month = "%0.2f" % (float(receive_per_month))
            transmit_per_month = "%0.2f" % (float(transmit_per_month))
            usage_per_month = "%0.2f" % usage_per_month

            msg = "%s usage: %0.2f%% (%s/%0.2fGB)" % (
                    interface,
                    usage_per_month_percent,
                    usage_per_month,
                    limit)

            if usage_per_month_percent < warning:
                func = self.ok
            elif warning <= usage_per_month_percent < critical:
                func = self.warning
            else:
                func = self.critical

            # check_linux_bandwidth_usage -i eth0 -W 50 -C 90 -d 10 -l 500 -f
            if args.perfdata and isinstance(warning, PercentValue) and limit is not None:

                p1 = PerfData(interface_percent,
                              used_total_percent,
                              unit="%",
                              warn=s_warning,
                              crit=s_critical,
                              min_="%0.2f" % (0),
                              max_="%0.2f" % (100))

                p2 = PerfData(interface_total,
                              usage_per_month,
                              unit="GB",
                              warn=warning,
                              crit=critical,
                              min_="%0.2f" % (0),
                              max_="%0.2f" % (limit))

                p3 = PerfData(interface_received,
                              receive_per_month,
                              unit="GB",
                              warn="",
                              crit="",
                              min_="%0.2f" % (0))

                p4 = PerfData(interface_transmitted,
                              transmit_per_month,
                              unit="GB",
                              warn="",
                              crit="",
                              min_="%0.2f" % (0))

            func(msg, p1, p2, p3, p4)

        # check_linux_bandwidth_usage -i eth0 -w 50 -c 100 -d 10 -l 500 -f
        if args.perfdata and args.limit is not None:
            # user give warning in GB so calculate in %
            usage_per_month_percent = (usage_per_month / limit) * 100

            msg = ("%s usage: %0.2f%% "
                   "(%0.2f/%0.2fGB)" % (interface,
                                        usage_per_month_percent,
                                        usage_per_month,
                                        limit))
            if usage_per_month < warning:
                func = self.ok
            elif usage_per_month >= warning and usage_per_month < critical:
                func = self.warning
            else:
                func = self.critical

            # convert all data to float with 2 decimal places
            warning_percent = "%0.2f" % ((float(warning) / limit) * 100)
            critical_percent = "%0.2f" % ((float(critical) / limit) * 100)
            used_total_percent = "%0.2f" % (usage_per_month_percent)
            warning = "%0.2f" % ((float(warning_percent) / 100) * limit)
            critical = "%0.2f" % ((float(critical_percent) / 100) * limit)
            usage_per_month = "%0.2f" % (float(usage_per_month))
            receive_per_month = "%0.2f" % (float(receive_per_month))
            transmit_per_month = "%0.2f" % (float(transmit_per_month))

            # create all perf data
            p1 = PerfData(interface_percent,
                          used_total_percent,
                          unit="%",
                          warn=warning_percent,
                          crit=critical_percent,
                          min_="%0.2f" % (0),
                          max_="%0.2f" % (100))

            p2 = PerfData(interface_total,
                          usage_per_month,
                          unit="GB",
                          warn=warning,
                          crit=critical,
                          min_="%0.2f" % (0),
                          max_="%0.2f" % (limit))

            p3 = PerfData(interface_received,
                          receive_per_month,
                          unit="GB",
                          warn="",
                          crit="",
                          min_="%0.2f" % (0))

            p4 = PerfData(interface_transmitted,
                          transmit_per_month,
                          unit="GB",
                          warn="",
                          crit="",
                          min_="%0.2f" % (0))

            func(msg, p1, p2, p3, p4)


        msg = "%s usage: %0.2fGB" % (interface, usage_per_month)
        # check_linux_bandwidth_usage -i eth0 -w 50 -c 90 -d 5
        if usage_per_month < warning:
            func = self.ok
        elif usage_per_month >= warning and usage_per_month < critical:
            func = self.warning
        else:
            func = self.critical

        # check_linux_bandwidth_usage -i eth0 -w 50 -c 90 -d 5 -f
        if args.perfdata:
            # convert all data to float with 2 decimal places
            receive_per_month = "%0.2f" % (float(receive_per_month))
            transmit_per_month = "%0.2f" % (float(transmit_per_month))
            usage_per_month = "%0.2f" % (float(usage_per_month))

            p1 = PerfData(interface_total,
                          usage_per_month,
                          unit="GB",
                          warn="%0.2f" % (warning),
                          crit="%0.2f" % (critical),
                          min_="%0.2f" % (0))

            p2 = PerfData(interface_received,
                          receive_per_month,
                          unit="GB",
                          warn="",
                          crit="",
                          min_="%0.2f" % (0))

            p3 = PerfData(interface_transmitted,
                          transmit_per_month,
                          unit="GB",
                          warn="",
                          crit="",
                          min_="%0.2f" % (0))

        func(msg, p1, p2, p3)


############################################################################

Plugin = CheckLinuxBandwidth

############################################################################

def main(argv=None):
    plugin = CheckLinuxBandwidth()
    plugin.execute(argv)


if __name__ == "__main__":
    main()
