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

from shinkenplugins import BasePlugin, PerfData, STATES
from lxml.etree import tostring
from lxml import etree
from decimal import *
import lxml.html
import urllib
import re


class Plugin(BasePlugin):
    NAME = 'check-hydro-quebec'
    VERSION = '0.1'
    DESCRIPTION = 'check interruptions for all Quebec'
    AUTHOR = 'vdnguyen'
    EMAIL = 'vanduc.nguyen@savoirfairelinux.com'
    # Can't touch this:
    ARGS = [('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            # Hammer time^W^W Add your plugin arguments here:
            # ('short', 'long', 'description', 'does it expect a value?')
            ('r', 'region', 'region to check', True),
            ('u', 'url', 'the url to fetch data from', True),
            ('w', 'warning', 'Limit to result in a warning state', True),
            ('c', 'critical', 'Limit to result in a critical state', True),
            ('l', 'list', 'the list of regions', False),
            ]

    URL = ("http://pannes.hydroquebec.com/"
           "pannes/bilan-interruptions-service/#bis")

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        # Handle show list of regions
        if 'list' in args:
            return True, None
        # Handle missing region argument
        if not args.get('region', None):
            args['region'] = u"Across Québec"
        else:
            # Format region name
            args['region'] = args.get('region').decode("utf-8")

        # Get region list
        result_dict = Plugin.create_result_dict()
        # Check if the region exist on Hydro Quebec site
        if 'critical' not in args and 'warning' not in args:
            if not args['region'] in result_dict.keys():
                msg_err = "Region '%s' unknown" % args['region']
                self.exit(STATES.UNKNOWN, msg_err)
            return True, None

        # Check critical argument
        if 'critical' not in args:
            self.exit(STATES.UNKNOWN, 'critical argument is missing')
        # Check warning argument
        if 'warning' not in args:
            self.exit(STATES.UNKNOWN, 'warning argument is missing')

        # Check float arguments
        float_arguments = ['warning',
                           'critical',
                           ]
        for argument_name in float_arguments:
            if argument_name in args:
                try:
                    args[argument_name] = float(args[argument_name])
                except:
                    return False, "bad format: `%s'" % argument_name

        # Arguments seems ok
        return True, None

    @staticmethod
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i: i + n]

    @staticmethod
    def create_result_dict():
        # Fetch page
        response = urllib.urlopen(Plugin.URL)
        # Read html
        page_source = response.read()
        # Parse html/xml
        root = lxml.html.fromstring(page_source)
        # Find all usefull tags
        raw_texts = root.xpath('//td//text()')
        # Chunk strings
        raw_texts = [i for i in Plugin.chunks(raw_texts, 5)]
        # Prepare result
        result_dict = {}
        # Trying to find data in texts
        for raw_text in raw_texts:
            if len(raw_text) == 5:
                # If the current line is a standard region
                # Get region name
                key = raw_text[0]
                # Get nb of interruptions
                interruptions = int(re.sub('[^\d]+', "", raw_text[2]))
                # Get nb of customers blackout
                customers_blackout = int(re.sub('[^\d]+', "", raw_text[3]))
                # Get nb of customers
                customers = int(re.sub('[^\d]+', "", raw_text[4]))
                # Store datas
                result_dict[key] = {'interruptions': interruptions,
                                    'customers_blackout': customers_blackout,
                                    'customers': customers}
            elif len(raw_text) == 3:
                # Special case for across Quebec
                # Set region "accross quebec"
                key = u"Across Québec"
                # Get nb of interruptions
                interruptions = int(re.sub('[^\d]+', "", raw_text[0]))
                # Get nb of customers blackout
                customers_blackout = int(re.sub('[^\d]+', "", raw_text[1]))
                # Get nb of customers
                customers = int(re.sub('[^\d]+', "", raw_text[2]))
                # Store datas
                result_dict[key] = {'interruptions': interruptions,
                                    'customers_blackout': customers_blackout,
                                    'customers': customers}
        return result_dict

    def run(self, args):
        # Get and parse datas
        result_dict = Plugin.create_result_dict()
        if 'list' in args:
            # Handle show region list
            output = "\n".join([r.encode("utf-8") for r in result_dict.keys()])
            # Exit showing region list
            self.exit(STATES.OK, 'regions:\n' + output)

        # Prepare warning
        if 'warning' in args:
            warning = args['warning']
        else:
            warning = 100.00

        # prepare critical
        if 'critical' in args:
            critical = args['critical']
        else:
            critical = 100.00

        # Get specified region dats
        customers_blackout = Decimal(result_dict[args['region']]['customers_blackout'])
        customers = Decimal(result_dict[args['region']]['customers'])
        interruptions = result_dict[args['region']]['interruptions']
        # Get percent
        percent = customers_blackout / customers * 100
        # Clean data
        round_percent = percent.quantize(Decimal('.01'),
                                         rounding=ROUND_HALF_UP)

        # Compare thresholds
        if round_percent < warning:
            msg = 'OK: %s: %0.2f%% out of service' % (args['region'],
                                                     round_percent)
            code = STATES.OK
        elif round_percent >= warning and round_percent < critical:
            msg = 'WARNING: %s: %0.2f%% out of service' % (args['region'],
                                                           round_percent)
            code = STATES.WARNING
        elif round_percent >= critical:
            msg = 'CRITICAL: %s: %0.2f%% out of service' % (args['region'],
                                                           round_percent)
            code = STATES.CRITICAL

        # Prepare perfdatas
        p1 = PerfData("percent_blackout",
                      round_percent,
                      unit="%",
                      warn=warning,
                      crit=critical,
                      min_=0,
                      max_=100)
        p2 = PerfData("interruptions",
                      interruptions,
                      unit='',
                      min_=0,
                      max_=None)
        p3 = PerfData("custumers_blackout",
                      customers_blackout,
                      unit='',
                      min_=0,
                      max_=customers)
        # Exit plugin
        self.exit(code, msg, p1, p2, p3)

if __name__ == "__main__":
    Plugin()
