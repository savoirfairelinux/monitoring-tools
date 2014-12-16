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


from shinkenplugins import BasePlugin, PerfData, STATES

class Plugin(BasePlugin):
    NAME = 'check-linux-bandwith-usage'
    VERSION = '0.1'
    DESCRIPTION = 'check linux bandwith usage per month'
    AUTHOR = 'vdnguyen'
    EMAIL = 'vanduc.nguyen@savoirfairelinux.com'

    ARGS = [# Can't touch this:
        ('h', 'help', 'display plugin help', False),
        ('v', 'version', 'display plugin version number', False),
        # Hammer time^W^W Add your plugin arguments here:
        # ('short', 'long', 'description', 'does it expect a value?')
        ('u', 'url', 'the url to fetch data from', True),
        ('w', 'warning', 'Limit to result in a warning state: GB', True),
        ('c', 'critical', 'Limit to result in a critical state: GB', True),
        ('i', 'interface-name', 'the name of interface you want to have a bandwith', True),
        ('l', 'limit', 'Limit of bandwith per month: GB', True),
        ('d', 'reset-day', 'number of day to reset the counter', True),
        ('s', 'cache-folder',
         'the folder to stock the data by default:/tmp/check_linux_bandwith/', True),
        ('f', 'perfdata', 'option to show perfdata', False),
        ('W', 'warning-percent', 'Limit to result in a warning state: %', True),
        ('C', 'critical-percent', 'Limit to result in a critical state: %', True),
        ]

    def check_args(self, args):
        """ Check arguments validity and set default values
        """
        interface_name = args.get("interface-name")
        # Interface name
        if not interface_name:
            # Interface name is missing
            self.exit(STATES.UNKNOWN, "Argument missing: --interface-name")
        if args.get("interface-name"):
            # Check if interface exists
            dev = open("/proc/net/dev", "r").readlines()
            interface_dict = {}
            for line in dev[2:]:
                intf = line[:line.index(":")].strip()
                interface_dict[intf] = [int(value) for value in line[line.index(":") + 1:].split()]

            if not interface_name in interface_dict:
                msg = ("There is not interface named: '%s'\n"
                       "Interfaces unavailable: :"
                       "%s" % (interface_name,
                               ", ".join(interface_dict.keys())
                              )
                      )
                self.exit(STATES.UNKNOWN, msg)

        # Check if limit argument is mandatory
        if args.get("warning-percent") and args.get("critical-percent") and not args.get("limit"):
            self.exit(STATES.UNKNOWN, "Missing limit argument")
        # Check if reset day is missing
        if not args.get("reset-day"):
            self.exit(STATES.UNKNOWN, "The day is missing")
        # Check if warning* is missing
        if not args.get("warning") and not args.get("warning-percent"):
            self.exit(STATES.UNKNOWN, "The warning argument is missing")
        # Check if critical* is missing
        if not args.get("critical") and not args.get("critical-percent"):
            self.exit(STATES.UNKNOWN, "The critical argument is missing")
        # Check if warning and warning-percent ar both defined
        if args.get("warning") and args.get("warning-percent"):
            self.exit(STATES.UNKNOWN, "Cannot put 2 warning arguments")
        # Check if critical and critical-percent ar both defined
        if args.get("critical") and args.get("critical-percent"):
            self.exit(STATES.UNKNOWN, "Cannot put 2 critical arguments")
        # Check warning and critical concordance
        if args.get("warning") and args.get("critical-percent"):
            self.exit(STATES.UNKNOWN,
                      "Cannot mix the warning number with critical percentage")
        # Check warning and critical concordance
        if args.get("warning-percent") and args.get("critical"):
            self.exit(STATES.UNKNOWN,
                      "Cannot mix the warning number with critical percentage")
        # Return
        return True, None

    @staticmethod
    def file_accessible(filepath, mode):
        try:
            f = open(filepath, mode)
            f.close()
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

    @staticmethod
    def get_total(interface):
        """ Get interface total bandwith
        """
        interface_dict = Plugin.get_interfaces_datas()
        receive = interface_dict[interface][0]
        transmit = interface_dict[interface][8]
        used_total = (float(receive) + float(transmit)) / (1024.0 ** 3)

        return used_total

    @staticmethod
    def get_receive(interface):
        # Get received data
        interface_dict = Plugin.get_interfaces_datas()
        receive = interface_dict[interface][0]
        receive = (float(receive)) / (1024.0 ** 3)

        return receive

    @staticmethod
    def get_transmit(interface):
        # Get transmit data
        interface_dict = Plugin.get_interfaces_datas()
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
        code = STATES.OK
        msg = ""
        # Get reset day
        day = int(args.get("reset-day"))
        # Get interface name
        interface = args["interface-name"]
        # Prepare interface variables

        # create a cache file
        if args.get("cache-folder"):
            cache_folder = args.get("cache-folder")
        else:
            cache_folder = "/tmp/check_linux_bandwith/"

        # Handle the last char of cache_folder
        if cache_folder[-1] != "/":
            cache_folder = cache_folder + "/"

        # create interface_file with the name of interface and the path
        interface_file = cache_folder + interface + ".txt"


        interface_total = interface + "_total"
        interface_percent = interface + "_percent"
        interface_received = interface + "_received"
        interface_transmitted = interface + "_transmitted"

        # Get warning
        if args.get("warning"):
            warning = float(args["warning"])
        # Get critical
        if args.get("critical"):
            critical = float(args["critical"])
        # Get warning percent
        warning_percent = 0.0
        if args.get("warning-percent"):
            warning_percent = float(args["warning-percent"])
        # Get critical percent
        critical_percent = 0.0
        if args.get("critical-percent"):
            critical_percent = float(args["critical-percent"])
        # Get limit
        limit = None
        if args.get("limit"):
            limit = float(args["limit"])

        # check if cache_folder exist if not create one
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)

        # if the file doesn't exist
        if not os.path.isfile(interface_file):
            try:
                int_fh = open(interface_file, "w")
            except IOError:
                self.exit(STATES.UNKNOWN,
                          "Cannot write temp file: %s" % interface_file)

            old_update = "00000000"
            # Get total
            used_total = Plugin.get_total(interface)
            offset = used_total
            # Get received
            receive_total = Plugin.get_receive(interface)
            receive_offset = Plugin.get_receive(interface)
            # Get transmit
            transmit_total = Plugin.get_transmit(interface)
            transmit_offset = Plugin.get_transmit(interface)
            # get old data
            old_data = Plugin.get_total(interface)
            old_receive = Plugin.get_receive(interface)
            old_transmit = Plugin.get_transmit(interface)
            # Write datas in file


            int_fh.write("%s %0.30f %0.30f %0.30f %0.30f "
                         "%0.30f %0.30f %0.30f %0.30f %0.30f" % (old_update,
                                                                 used_total,
                                                                 offset,
                                                                 receive_total,
                                                                 receive_offset,
                                                                 transmit_total,
                                                                 transmit_offset,
                                                                 old_data,
                                                                 old_receive,
                                                                 old_transmit))
            # Close file
            int_fh.close()
            # Exit for the first launch
            self.exit(code, "First use of plugin")

        else:
            try:
                int_fh = open(interface_file, "r+")
            except IOError:
                self.exit(STATES.UNKNOWN,
                          "Cannot read/write temp file: %s" % interface_file)
            # read file
            data_list = int_fh.readline()
            # prepare read datas
            data_list = data_list.strip().split()
            # get new datas
            new_used = Plugin.get_total(interface)
            new_receive = Plugin.get_receive(interface)
            new_transmit = Plugin.get_transmit(interface)
            # get data
            old_update = data_list[0]
            # get totals
            used_total = float(data_list[1])
            receive_total = float(data_list[3])
            transmit_total = float(data_list[5])
            # Get offsets
            offset = float(data_list[2])
            receive_offset = float(data_list[4])
            transmit_offset = float(data_list[6])
            # get old datas
            old_data = float(data_list[7])
            old_receive = float(data_list[8])
            old_transmit = float(data_list[9])
            # get reset date
            reset_date = Plugin.get_reset_day(day)
            # Get today
            to_day = time.strftime("%m%d%Y")
            # Check if the counter restarted

            if new_used >= used_total:
                used_total = new_used
                receive_total = new_receive
                transmit_total = new_transmit

            else:
                # Handle counter restart
                if new_used >= old_data:
                    used_total = used_total + (new_used - old_data)
                    receive_total = receive_total + (new_receive - old_receive)
                    transmit_total = transmit_total + (new_transmit - old_transmit)
                else:
                    used_total = used_total + new_used
                    receive_total = receive_total + new_receive
                    transmit_total = transmit_total + new_transmit

            # get all data to update storage file
            old_data = new_used
            old_receive = new_receive
            old_transmit = new_transmit
            # get all data for output
            usage_per_month = used_total - offset
            receive_per_month = receive_total - receive_offset
            transmit_per_month = transmit_total - transmit_offset
            # check if to day is reset date
            if to_day == reset_date and to_day != old_update:
                offset = used_total
                receive_offset = receive_total
                transmit_offset = transmit_total
                old_update = reset_date
            # write data to file
            int_fh.seek(0)
            int_fh.write("%s %0.30f %0.30f %0.30f %0.30f "
                         "%0.30f %0.30f %0.30f %0.30f %0.30f" % (old_update,
                                                                 used_total,
                                                                 offset,
                                                                 receive_total,
                                                                 receive_offset,
                                                                 transmit_total,
                                                                 transmit_offset,
                                                                 old_data,
                                                                 old_receive,
                                                                 old_transmit))
            int_fh.close()

        # check_linux_bandwith_usage -i eth0 -W 50 -C 90 -d 10 -l 500
        if args.get("limit") and args.get("warning-percent"):

            warning_percent = float(args.get("warning-percent"))
            critical_percent = float(args.get("critical-percent"))
            # calculate bandwidth per month in %
            usage_per_month_percent = (usage_per_month / limit) * 100
            # user does not give warning in GB so we have to calculate it
            warning = "%0.2f" % ((float(warning_percent) / 100) * limit)
            critical = "%0.2f" % ((float(critical_percent) / 100) * limit)
            # convert all data to float with 2 decimal places
            receive_per_month = "%0.2f" % (float(receive_per_month))
            transmit_per_month = "%0.2f" % (float(transmit_per_month))
            usage_per_month = "%0.2f" % usage_per_month

            if usage_per_month_percent < warning_percent:
                msg = ("OK: %s usage: %0.2f%% "
                       "(%s/%0.2fGB)" % (interface,
                                         usage_per_month_percent,
                                         usage_per_month,
                                         limit))
                code = STATES.OK
            elif usage_per_month_percent >= warning_percent and usage_per_month_percent < critical_percent:
                msg = ("WARNING: %s usage: %0.2f%% "
                       "(%s/%0.2fGB)" % (interface,
                                         usage_per_month_percent,
                                         usage_per_month,
                                         limit))
                code = STATES.WARNING
            elif usage_per_month_percent >= critical_percent:
                msg = ("CRITICAL: %s usage: %0.2f%% "
                       "(%s/%0.2fGB)" % (interface,
                                         usage_per_month_percent,
                                         usage_per_month,
                                         limit))
                code = STATES.CRITICAL

            # check_linux_bandwith_usage -i eth0 -W 50 -C 90 -d 10 -l 500 -f
            if "perfdata" in args.keys() and args.get("warning-percent") and args.get("limit"):

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

            self.exit(code, msg, p1, p2, p3, p4)

        # check_linux_bandwith_usage -i eth0 -w 50 -c 100 -d 10 -l 500 -f
        if "perfdata" in args.keys() and args.get("warning") and args.get("limit"):
            # get all data from args
            limit = float(args.get("limit"))
            warning = float(args.get("warning"))
            critical = float(args.get("critical"))
            # user give warning in GB so calculate in %
            usage_per_month_percent = (usage_per_month / limit) * 100

            if usage_per_month < warning:
                msg = ("OK: %s usage: %0.2f%% "
                       "(%0.2f/%0.2fGB)" % (interface,
                                            usage_per_month_percent,
                                            usage_per_month,
                                            limit))
                code = STATES.OK
            elif usage_per_month >= warning and usage_per_month < critical:
                msg = ("WARNING: %s usage: %0.2f%% "
                       "(%0.2f/%0.2fGB)" % (interface,
                                            usage_per_month_percent,
                                            usage_per_month,
                                            limit))
                code = STATES.WARNING
            elif usage_per_month >= critical:
                msg = ("CRITICAL: %s usage: %0.2f%% "
                       "(%0.2f/%0.2fGB)" % (interface,
                                            usage_per_month_percent,
                                            usage_per_month,
                                            limit))
                code = STATES.CRITICAL

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

            self.exit(code, msg, p1, p2, p3, p4)

        # check_linux_bandwith_usage -i eth0 -w 50 -c 90 -d 5
        if args.get("warning"):
            warning = float(args.get("warning"))
            critical = float(args.get("critical"))

            if usage_per_month < warning:
                msg = "OK: %s usage: %0.2fGB" % (interface, usage_per_month)
                code = STATES.OK
            elif usage_per_month >= warning and usage_per_month < critical:
                msg = "WARNING: %s usage: %0.2fGB" % (interface, usage_per_month)
                code = STATES.WARNING
            elif usage_per_month >= critical:
                msg = "CRITICAL: %s usage: %0.2fGB" % (interface, usage_per_month)
                code = STATES.CRITICAL

            # check_linux_bandwith_usage -i eth0 -w 50 -c 90 -d 5 -f
            if "perfdata" in args.keys() and args.get("warning"):
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

            self.exit(code, msg, p1, p2, p3)

if __name__ == "__main__":
    Plugin()
