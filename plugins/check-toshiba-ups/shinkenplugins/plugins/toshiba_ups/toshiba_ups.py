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
#               2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import

import os
import os.path
import time
import datetime
import argparse
import warnings

import getopt
import sys

from pysnmp.entity.rfc3413.oneliner import cmdgen

import re

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin

class CheckToshibaUps(ShinkenPlugin):
    NAME = 'toshiba_ups'
    VERSION = '1.0'
    DESCRIPTION = 'Plugin to check Toshiba UPSs'
    AUTHOR = 'Thibault Cohen'
    EMAIL = 'thibault.cohen@savoirfairelinux.com'

    CHECK_TYPES = {
                'output_percent': '.1.3.6.1.4.1.4550.1.1.4.4.1.5',  # table
                'battery_status': '.1.3.6.1.4.1.4550.1.1.2.1',  # table
                'input_volt': '.1.3.6.1.4.1.4550.1.1.3.3.1.3',  # table
                'output_volt': '.1.3.6.1.4.1.4550.1.1.4.4.1.2',  # table
                'battery_temperature': '.1.3.6.1.4.1.4550.1.1.2.7.0',  # table
                'emc_temperature': '.1.3.6.1.4.1.186.1.19.2.1.15.2.0', # leaf
                }

    def __init__(self):
        super(CheckToshibaUps, self).__init__()
        self.add_warning_critical()
        self.parser.add_argument('--hostname', '-H', required=True, help='Host name, IP Address')
        self.parser.add_argument('--community', '-C', help='SNMP community, default: public', default="public")
        self.parser.add_argument('--snmpversion', '-V', help='SNMP version, "1", "2" or "2c', default="2c")
        self.parser.add_argument('--check_type', '-t', help='What you want to check : '
                                 '"output_percent", "battery_status", "input_volt",'
                                 '"output_volt", "temperature"',
                                 required=True)




    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckToshibaUps, self).parse_args(args)
        if None in (args.warning, args.critical) and args.check_type != 'battery_status':
            self.parser.error('--warning and --critical are both required')

        if args.check_type not in self.CHECK_TYPES:
            self.parser.error("Bad value for 'check_type' argument: %s."
                              "Specify one of the following %s" %
                              (args.check_type, self.CHECK_TYPES.keys()))

        return args

    def get_output_percent(self, args, values):

        try:
            values = [(str(k), int(str(v))) for k, v in values]
        except Exception:
            self.unknown("Can't parse data for output percent")

        critical = False
        warning = False
        msg = ""
        perfdatas = []
        for oid, val in values:
            if val >= args.critical:
                if not critical:
                    msg = "Output percent - Critical threshold %d%%" % args.critical
                msg += " - Unit%s: %d%%" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                critical = True
            elif val >= args.warning and not critical:
                if not warning:
                    msg = "Output percent - Warning threshold %d%%" % args.warning
                msg += " - Unit%s: %d%%" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                warning = True
            elif not warning and not critical:
                if msg == "":
                    msg = "Output percent"
                msg += " - Unit%s: %d%%" % (oid[-1], val)  #The last char is a number and is picked identify the Unit

            perfdatas.append(PerfData("Unit%s" % oid[-1], val, unit="%", min_=0))

        if critical:
            self.critical(msg, *perfdatas)
        elif warning:
            self.warning(msg, *perfdatas)
        else:
            self.ok(msg, *perfdatas)


    def get_battery_status(self, args, values):

        if len(values) != 1:
            self.unknown("Only one battery is managed now sorry")

        try:
            out = int(str(values[0][1]))
        except Exception:
            self.unknown("Can't parse data for battery status")

        perfdatas = [PerfData("Status", out)]

        if out == 1:
            self.critical("Battery status UNKNOWN", *perfdatas)
        elif out == 2:
            self.ok("Battery Status Normal", *perfdatas)
        elif out == 3:
            self.critical("Battery Status : LOW", *perfdatas)
        elif out == 4:
            self.critical("Battery Status : DEPLETED", *perfdatas)
        else:
            self.unknown('Plugin ERROR')


    def get_input_volt(self, args, values):

        try:
            values = [(str(k), int(str(v))) for k, v in values]
        except Exception:
            self.unknown("Can't parse data for output percent")

        critical = False
        warning = False
        msg = ""
        perfdatas = []
        for oid, val in values:
            if val >= args.critical:
                if not critical:
                    msg = "Input Volt - Critical threshold  %d RMS Volts" % args.critical
                msg += " - Unit%s: %d RMS Volts" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                critical = True
            elif val >= args.warning and not critical:
                if not warning:
                    msg = "Input Volt - Warning threshold  %d RMS Volts" % args.warning
                msg += " - Unit%s: %d RMS Volts" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                warning = True
            elif not warning and not critical:
                if msg == "":
                    msg = "Input Volt"
                msg += " - Unit%s: %d RMS Volts" % (oid[-1], val)  #The last char is a number and is picked identify the Unit

            perfdatas.append(PerfData("Unit%s" % oid[-1], val, unit="V", min_=0))

        if critical:
            self.critical(msg, *perfdatas)
        elif warning:
            self.warning(msg, *perfdatas)
        else:
            self.ok(msg, *perfdatas)


    def get_output_volt(self, args, values):
        try:
            values = [(str(k), int(str(v))) for k, v in values]
        except Exception:
            self.unknown("Can't parse data for output percent")

        critical = False
        warning = False
        msg = ""
        perfdatas = []
        for oid, val in values:
            if val >= args.critical:
                if not critical:
                    msg = "Output Volt - Critical threshold  %d RMS Volts" % args.critical
                msg += " - Unit%s: %d RMS Volts" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                critical = True
            elif val >= args.warning and not critical:
                if not warning:
                    msg = "Output Volt - Warning threshold  %d RMS Volts" % args.warning
                msg += " - Unit%s: %d RMS Volts" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                warning = True
            elif not warning and not critical:
                if msg == "":
                    msg = "Output Volt"
                msg += " - Unit%s: %d RMS Volts" % (oid[-1], val)  #The last char is a number and is picked identify the Unit

            perfdatas.append(PerfData("Unit%s" % oid[-1], val, unit="V", min_=0))

        if critical:
            self.critical(msg, *perfdatas)
        elif warning:
            self.warning(msg, *perfdatas)
        else:
            self.ok(msg, *perfdatas)

    def get_battery_temperature(self, args, values):
        try:
            values = [(str(k), float(str(v))) for k, v in values]
        except Exception:
            self.unknown("Can't parse data for battery temperature")

        critical = False
        warning = False
        msg = ""
        perfdatas = []
        for oid, val in values:
            if val >= args.critical:
                if not critical:
                    msg = "Battery Temperature - Critical threshold  %d Celsius" % args.critical
                msg += " - Unit%s: %dC" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                critical = True
            elif val >= args.warning and not critical:
                if not warning:
                    msg = "Battery Temperature - Warning threshold  %d Celsius" % args.warning
                msg += " - Unit%s: %dC" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                warning = True
            elif not warning and not critical:
                if msg == "":
                    msg = "Battery Temperature"
                msg += " - Unit%s: %dC" % (oid[-1], val)  #The last char is a number and is picked identify the Unit

            perfdatas.append(PerfData("Unit%s" % oid[-1], val, unit="C", min_=0))

        if critical:
            self.critical(msg, *perfdatas)
        elif warning:
            self.warning(msg, *perfdatas)
        else:
            self.ok(msg, *perfdatas)


    def get_emc_temperature(self, args, values):
        try:
            values = [(str(k), float(str(v))/10.0) for k, v in values]  # Value is XXX for XX.X
        except Exception:
            self.unknown("Can't parse data for emc temperature")

        critical = False
        warning = False
        msg = ""
        perfdatas = []
        for oid, val in values:
            if val >= args.critical:
                if not critical:
                    msg = "EMC Temperature - Critical threshold  %d Celsius" % args.critical
                msg += " - Unit%s: %0.1fC" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                critical = True
            elif val >= args.warning and not critical:
                if not warning:
                    msg = "EMC Temperature - Warning threshold  %d Celsius" % args.warning
                msg += " - Unit%s: %0.1fC" % (oid[-1], val)  #The last char is a number and is picked identify the Unit
                warning = True
            elif not warning and not critical:
                if msg == "":
                    msg = "EMC Temperature"
                msg += " - Unit%s: %0.1fC" % (oid[-1], val)  #The last char is a number and is picked identify the Unit

            perfdatas.append(PerfData("Unit%s" % oid[-1], val, unit="C", min_=0))

        if critical:
            self.critical(msg, *perfdatas)
        elif warning:
            self.warning(msg, *perfdatas)
        else:
            self.ok(msg, *perfdatas)

    def run(self, args):
        """ Main Plugin function """
        check_type = args.check_type
        hostname = args.hostname
        version = args.snmpversion
        community = args.community

        generator = cmdgen.CommandGenerator()
        comm_data = cmdgen.CommunityData('server', community, 0)
        transport = cmdgen.UdpTransportTarget((hostname, 161))

        (errorIndication,errorStatus, errorIndex, varBind) = generator.getCmd(comm_data, transport, self.CHECK_TYPES[check_type])


        # Results = [("OID", "VALUE"),...]
        results = []
        for oid, val in varBind:
            match = re.search(self.CHECK_TYPES[check_type][1:], str(oid))  # Remove the first "."
            if match:
                results.append((oid, val))  # We can ask a table so we have to get all of them
                break

        if len(results) == 0:
            self.unknown("Not data found for the following oid : '%s'. Maybe the oid does not exist"
                         % self.CHECK_TYPES[check_type])

        handle_perf = getattr(self, 'get_' + check_type, None)

        if handle_perf:
            handle_perf(args, results)
        else:
            self.unknown("Cannot handle this mode %s" % check_type)



############################################################################

Plugin = CheckToshibaUps

############################################################################

def main(argv=None):
    plugin = CheckToshibaUps()
    plugin.execute(argv)


if __name__ == "__main__":
    main()