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

# Copyright (C) 2014, Thibault Cohen <thibault.cohen@savoirfairelinux.com>

import os
import glob
from datetime import datetime, timedelta
import json
import re
import sys


from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi.exval import noSuchInstance



from shinkenplugins import BasePlugin, PerfData, STATES

MSG = ''
PERF_MSG = ''


IF_STATUS = {1: 'UP',
             2: 'DOWN',
             3: 'TESTING',
             4: 'UNKNOWN',
             5: 'DORMANT',
             6: 'NotPresent',
             7: 'lowerLayerDown'}

def convert_octets(octets):
    """Convert octets to kilo octets, mega octsts, giga octets """
    i = 0
    while octets > 1024:
        octets = octets / 1024.0
        i = i + 1

    unit = {0: 'Bps', 1: 'KBps', 2: 'MBps', 3: 'GBps'}

    return (octets, unit[i])


def append_msg(msg):
    """Appent text to output
    """
    global MSG
    if MSG != "":
        MSG = " ".join((MSG, msg))
    else:
        MSG = msg


def append_perf(msg):
    """Append text to perf data
    """
    global PERF_MSG
    if PERF_MSG != "":
        PERF_MSG = " ".join((PERF_MSG, msg))
    else:
        PERF_MSG = msg


def print_output(kargs):
    """Print output for Nagios
    """
    if MSG == '':
        print "Nothing to print"
    elif kargs['perf']:
        print " ".join((MSG, "|", PERF_MSG))
    else:
        print "%s" % MSG

class Plugin(BasePlugin):
    NAME = 'check-snmp-interface'
    VERSION = '0.1'
    DESCRIPTION = 'This plugin check interface traffic using SNMP'
    AUTHOR = 'Thibault Cohen'
    EMAIL = 'thibault.cohen@savoirfairelinux.com'
    # Datas for SNMP
    OID_IFNUMBER = '.1.3.6.1.2.1.2.1.0'
    OIDS = {
        '.1.3.6.1.2.1.2.2.1.1': 'index',  # index_table
        '.1.3.6.1.2.1.2.2.1.2': 'descr',  # descr_table
        '.1.3.6.1.2.1.2.2.1.5': 'speed',  # speed_table
        '.1.3.6.1.2.1.2.2.1.7': 'admin',  # admin_table
                                          # set by user (what the user want)
                                          # 1-UP, 2-DOWN, 3-TESTING
        '.1.3.6.1.2.1.2.2.1.8': 'oper',  # oper_table
                                         # the actual state
                                         # 1-UP, 2-DOWN, 3-TESTING
        '.1.3.6.1.2.1.2.2.1.10': 'in_octet',  # in_octet_table
        '.1.3.6.1.2.1.2.2.1.13': 'in_discard',  # in_discard_table
        '.1.3.6.1.2.1.2.2.1.14': 'in_error',  # in_error_table
        '.1.3.6.1.2.1.2.2.1.16': 'out_octet',  # out_octet_table
        '.1.3.6.1.2.1.2.2.1.19': 'out_discard',  # out_discard_table
        '.1.3.6.1.2.1.2.2.1.20': 'out_error',  # out_discard_table
        '.1.3.6.1.2.1.31.1.1.1.15': 'speed_64',  # speed_table_64
        '.1.3.6.1.2.1.31.1.1.1.6': 'in_octet_64',  # in_octet_table_64
        '.1.3.6.1.2.1.31.1.1.1.10': 'out_octet_64',  # out_octet_table_64
    }
    IF_STATUS = {1: 'UP',
                 2: 'DOWN',
                 3: 'TESTING',
                 4: 'UNKNOWN',
                 5: 'DORMANT',
                 6: 'NotPresent',
                 7: 'lowerLayerDown'}

    # Arguments
    ARGS = [# Can't touch this:
            ('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            # Host address
            ('H',
             'host-address',
             'Host address IP',
             True),
            # SNMP snmp-community
            ('C',
             'snmp-community',
             ('SNMP community\n'
              '    Optional; Default: public'),
             True),
            # SNMP version
            ('V',
             'snmp-version',
             ('SNMP version\n'
              '    Optional; Default: 2c'),
             True),
            # SNMP Port
            ('P',
             'port',
             ('SNMP port\n'
              '    Optional; Default: 161'),
             True),
            # SNMP Timeout
            ('T',
             'timeout',
             ('SNMP timeout\n'
              '    Optional; Default: 3'),
             True),
            # Cache Folder
            ('F',
             'cache-folder',
             ('Folder where cache will be store\n'
              '    Optional; Default: /tmp/check_snmp_int/'),
             True),
            # Interface name
            ('l',
             'list-interfaces',
             ('List all interfaces name'),
             False),
            # Interface name
            ('n',
             'ifname',
             ('Interface name regexp to match\n'
              '    Optional; Default: * (match all)'),
             True),
            # Update time
            ('u',
             'update-time',
             ('Seconds between two fetches\n'
              '    Optional; Default: 60'),
             True),
            # Check traffic errors
            ('e',
             'error',
             ('Add error & discard to Perfparse output\n'
              '    Optional; Default: False'),
             False),
            # Check input/ouput
            ('k',
             'perfcheck',
             ('check the input/ouput bandwidth of the interface.\n'
              '    Optional; Default: False'),
             False),
            # Show perfdata
            ('f',
             'perfdata',
             ('Perfdata compatible output (no output when interface is down).\n'
              '    Optional; Default: False'),
             False),
            # Warning
            ('w',
             'warning',
             ('Warning threshold\n'
              '    Optional; Default: None'),
             True),
            # Critical
            ('c',
             'critical',
             ('Critical threshold\n'
              '    Optional; Default: None'),
             True),
            # Realbandwidth
            ('b',
             'realbandwidth',
             ('Set real bandwidth in bps (bits per second)\n'
              '    Optional; Default: guessed from SNMP'),
             True),
            # Only UP
            ('o',
             'only-up',
             ('Show only interfaces in UP state\n'
              '    Optional; Default: False'),
             False),
            # 64 bits
            ('g',
             '64bits',
             ('Use 64 bits counters\n'
              '    Optional; Default: False'),
             False),
            ]

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        mandatory_arguments = ['host-address',
                              ]
        for argument_name in mandatory_arguments:
            if not argument_name in args.keys():
                return False, "Argument `%s' is missing !" % argument_name

        # Handle default values
        if not 'snmp-community' in args.keys():
            args['snmp-community'] = 'public'

        if not 'snmp-version' in args.keys():
            args['snmp-version'] = '2c'

        if not 'port' in args.keys():
            args['port'] = '161'

        if not 'timeout' in args.keys():
            args['timeout'] = 3

        if not 'cache-folder' in args.keys():
            args['cache-folder'] = '/tmp/check_snmp_int/'

        if not 'ifname' in args.keys():
            args['ifname'] = ''

        if not 'error' in args.keys():
            args['error'] = False

        if not 'perfcheck' in args.keys():
            args['perfcheck'] = False

        if not 'perfdata' in args.keys():
            args['perfdata'] = False

        if not 'update-time' in args.keys():
            args['update-time'] = 60

        if not 'realbandwidth' in args.keys():
            args['realbandwidth'] = False

        if not 'list-interfaces' in args.keys():
            args['list-interfaces'] = False

        if not 'only-up' in args.keys():
            args['only-up'] = False

        if not '64bits' in args.keys():
            args['64bits'] = False

        # Set boolean
        boolean_args = ['error',
                        'perfcheck',
                        'perfdata',
                        'realbandwidth',
                        'list-interfaces',
                        'only-up',
                        '64bits']
        for argument_name in boolean_args:
            if args[argument_name] == '':
                args[argument_name] = True

        # SNMP version
        if args['snmp-version'] not in ['1', '2c']:
            return False, "Bad SNMP Version!" % argument_name

        # Int arguments
        int_arguments = ['update-time',
                         'realbandwidth',
                         'port',
                        ]
        for argument_name in int_arguments:
            try:
                args[argument_name] = int(args[argument_name])
            except ValueError:
                return False , "Argument `%s' is mal formatted!" % argument_name

        # Set cache_folder
        self.cache_folder = args['cache-folder']

        return True, None


    def save_interface(self, interface):
        """Save to file
        """
        f = open(os.path.join(self.cache_folder,
                              str(interface['host']) + "_" + str(interface['descr']).replace("/", "_")),
                              'wb')
        json.dump(interface, f)
        f.close()

    def load_interface(self, file_name):
        """Save to file
        """
        f = open(file_name)
        interface = json.load(f)
        f.close()
        return interface

    def compute_output(self, interface, args):
        """Prepare output
        """
        perf_datas = []
        # If show only up enabled and interface down
        # Doesn't it it in output
        if args['only-up'] and interface['oper'] != 1:
            return

        seconds = int(interface.get('date', 0)) - int(interface.get('old_date', 0))
        # seconds == 0, it's impossible
        if seconds == 0:
            return STATES.OK, "Waiting next check" 

        output_datas = {}
        output_datas['name'] = interface['descr']
        # HANDLE COUNTER RESET
        ## Set limit
        ## 32bits : 4294967295
        ## 64bits : 18446744073709551615
        if args['64bits']:
            # Check 64Bits support
            if self.out_octet_64 is None or self.in_octet_64 is None:
                print "This device doesn't support 64bits counters"
                sys.exit(STATE_UNKNOWN)
            limit = 18446744073709551615
            in_counter_name = "in_octet_64"
            out_counter_name = "out_octet_64"
            old_in_counter_name = "old_in_octet_64"
            old_out_counter_name = "old_out_octet_64"
        else:
            limit = 4294967295
            in_counter_name = "in_octet"
            out_counter_name = "out_octet"
            old_in_counter_name = "old_in_octet"
            old_out_counter_name = "old_out_octet"
        ## Calc and handle Reset
        ### IN
        if int(interface.get(old_in_counter_name, 0)) > int(interface.get(in_counter_name, 0)):
            in_octets = limit - int(interface.get(old_in_counter_name, 0)) + int(interface.get(in_counter_name, 0))
        else:
            in_octets = int(interface.get(in_counter_name, 0)) - int(interface.get(old_in_counter_name, 0))
        ### OUT
        if int(interface.get(old_out_counter_name, 0)) > int(interface.get(out_counter_name, 0)):
            out_octets = limit - int(interface.get(old_out_counter_name, 0)) + int(interface.get(out_counter_name, 0))
        else:
            out_octets = int(interface.get(out_counter_name, 0)) - int(interface.get(old_out_counter_name, 0))

        output_datas['raw_in_bandwidth'] = in_octets / seconds
        output_datas['raw_out_bandwidth'] = out_octets / seconds
        output_datas['in_bandwidth'], output_datas['in_unit'] = convert_octets(
                                                    output_datas['raw_in_bandwidth'])
        output_datas['out_bandwidth'], output_datas['out_unit'] = convert_octets(
                                                    output_datas['raw_out_bandwidth'])

        output_datas['state'] = IF_STATUS[interface.get('oper', 2)]
        if args['realbandwidth']:
            interface['speed'] = args['realbandwidth']
        # bit to byte
        output_datas['speed'] = interface['speed'] / 8.0

        msg = ("%(name)s:%(state)s "
               "(%(in_bandwidth).2f%(in_unit)s/"
               "%(out_bandwidth).2f%(out_unit)s)"
               % output_datas)

        output_datas['name'] = output_datas['name'].replace(" ", "_")

        if args['perfdata']:
            # handle one interface
            perf_datas.append(PerfData('%(name)s_in_Bps' % output_datas,
                              '%(raw_in_bandwidth)0.2f' % output_datas,
                              unit='Bps',
                              min_=0.0))
            perf_datas.append(PerfData('%(name)s_out_Bps' % output_datas,
                              '%(raw_out_bandwidth)0.2f' % output_datas,
                              unit='Bps',
                              min_=0.0))
            if output_datas['speed'] != 0:
                output_datas['prct_in'] = output_datas['raw_in_bandwidth'] * 100 / output_datas['speed']
                output_datas['prct_out'] = output_datas['raw_out_bandwidth'] * 100 / output_datas['speed']
                # Put % data in first for Nagvis
                perf_datas.insert(0,
                                  PerfData('%(name)s_in_prct' % output_datas,
                                           '%(prct_in)0.2f' % output_datas,
                                           '%',
                                           min_=0.0,
                                           max_=100.0))
                perf_datas.insert(0,
                                  PerfData('%(name)s_out_prct' % output_datas,
                                           '%(prct_out)0.2f' % output_datas,
                                           '%',
                                           min_=0.0,
                                           max_=100.0))

            if args['error']:
                output_datas['raw_in_discard'] = self.in_discard
                output_datas['raw_out_discard'] = self.out_discard
                perf_datas.append(PerfData('%(name)s_in_discard' % output_datas,
                                           '%(raw_in_discard)0.2f' % output_datas,
                                           'c'))
                perf_datas.append(PerfData('%(name)s_out_discard' % output_datas,
                                           '%(raw_out_discard)0.2f' % output_datas,
                                           'c'))
                output_datas['raw_in_error'] = self.in_error
                output_datas['raw_out_error'] = self.out_error
                perf_datas.append(PerfData('%(name)s_in_error' % output_datas,
                                           '%(raw_in_error)0.2f' % output_datas,
                                           'c'))
                perf_datas.append(PerfData('%(name)s_out_error' % output_datas,
                                           '%(raw_out_error)0.2f' % output_datas,
                                           'c'))

        return STATES.OK, msg, perf_datas



    def find_data(self, args, interfaces={}):
        """Search if data was already fetched """
        host_address = args['host-address']
        ifname = args['ifname']
        update_time = args['update-time']
        cache_folder = args['cache-folder']

        # Check if cache file exists
        if not os.path.exists(cache_folder):
            return True, interfaces
        if len(glob.glob(cache_folder + "/" + host_address + ":*")):
            return True, interfaces

        if interfaces == {}:
            files = os.listdir(cache_folder)
            # First launch
            if len(files) == 0:
                return True, interfaces
            # Read cache files
            for fname in files:
                if fname.startswith(host_address + "_"):
                    if re.search(ifname, fname.split(host_address + "_")[-1]) or re.search(ifname.replace("/", "_"), fname.split(host_address + "_")[-1]):
                        filename = os.path.join(cache_folder, fname)
                        interface = self.load_interface(filename)
                        if interface:
                            interfaces[interface['index']] = interface

        if interfaces == {}:
            return True, interfaces

        # Prepare output
        messages = []
        states = []
        perfdatas = []
        now = datetime.now()
        # Prepare results
        for interface in interfaces.values():
            if re.search(ifname, str(interface.get('descr'))) or re.search(ifname.replace("/", "_"), str(interface.get('descr'))):
                last_update = datetime.fromtimestamp(int(interface.get('date', 0)))
                if last_update + timedelta(0, update_time) < now:
                    return True, interfaces
                if interface.get('old_date') is None:
                    return True, interfaces
                
                output = self.compute_output(interface, args)
                if output is None:
                    continue
                states.append(output[0])
                messages.append(output[1])
                perfdatas.extend(output[2])
        
        # Output
        self.exit(max(states), " # ".join(messages), *perfdatas)

    def format_results(self, results, interfaces):
        """ format results
        """
        for results_by_interface in results:
            temp_int = {}
            for results in results_by_interface:
                snmp_table, index = str(results[0]).rsplit(".", 1)
                index = int(index)
                # Test if the interfaces is new or not
                if index in interfaces:
                    temp_int = interfaces[index]

                snmp_table = "." + snmp_table
                if snmp_table in self.OIDS:
                    attr_name = self.OIDS[snmp_table]
                else:
                    continue

                # Set old data
                temp_int["old_" + attr_name] = temp_int.get(attr_name)

                # Set new data
                try:
                    temp_int[attr_name] = int(results[1])
                except (ValueError, AttributeError):
                    temp_int[attr_name] = str(results[1])

            temp_int['old_date'] = temp_int.get('date')
            temp_int['date'] = datetime.now().strftime("%s")
            interfaces[index] = temp_int
                

        return interfaces


    def fetch_data(self, args, interfaces={}):
        """Fetch data from host
        """
        host_address = args['host-address']
        community = args['snmp-community']
        version = args['snmp-version']
        ifname = args['ifname']
        error = args['error']
        realbandwidth = args['realbandwidth']
        cache_folder = args['cache-folder']
        interfaces_res ={}

        # Check if tmp folder exists
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        else:
            files = os.listdir(cache_folder)
            for fname in files:
                if fname.startswith(host_address + "_"):
                    filename = os.path.join(cache_folder, fname)
                    interface = self.load_interface(filename)
                    if interface:
                        interfaces[interface['index']] = interface

        # Prepare snmp command
        snmp_cmdgen = cmdgen.CommandGenerator()

        # Prepare snmp data
        pysnmp_community = cmdgen.CommunityData(args['snmp-community'])
        pysnmp_target = cmdgen.UdpTransportTarget((args['host-address'], args['port']),
                                                  timeout=args['timeout'],
                                                  retries=0)
        pysnmp_oid = [str(oid) for oid in self.OIDS.keys()]
        # Get snmp datas
        (errorIndication,
         errorStatus,
         errorIndex,
         varBind) = snmp_cmdgen.nextCmd(pysnmp_community,
                                       pysnmp_target,
                                       *pysnmp_oid)
        # TODO Handle errors
        if errorIndication:
            pass
        if errorStatus != 0:
            pass
        if errorIndex != 0:
            pass

        # Format result
        interfaces_raw = self.format_results(varBind, interfaces)

        # Save to disk
        for index, interface in interfaces_raw.items():
            interface['host'] = args['host-address']
            self.save_interface(interface)

        return interfaces_res



    def list_interface(self, args):
        # Prepare snmp command
        snmp_cmdgen = cmdgen.CommandGenerator()

        # Prepare snmp data
        pysnmp_community = cmdgen.CommunityData(args['snmp-community'])
        pysnmp_target = cmdgen.UdpTransportTarget((args['host-address'], args['port']),
                                                  timeout=args['timeout'],
                                                  retries=0)
        # Get snmp datas
        (errorIndication,
         errorStatus,
         errorIndex,
         varBind) = snmp_cmdgen.nextCmd(pysnmp_community,
                                        pysnmp_target,
                                        ".1.3.6.1.2.1.2.2.1.2")

        # TODO Handle errors
        if errorIndication:
            pass
        if errorStatus != 0:
            pass
        if errorIndex != 0:
            pass

        # Format result
        interface_list = [str(row[0][1]) for row in varBind]

        return "\n".join(interface_list)

    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        if args['list-interfaces']:
            message = self.list_interface(args)
            self.exit(STATES.UNKNOWN, message)

        action, interfaces = self.find_data(args)

        if action:
            interfaces = self.fetch_data(args, interfaces)
            self.find_data(args, interfaces)
            


        self.exit(STATES.OK, "Please wait the next check")

if __name__ == "__main__":
    Plugin()
