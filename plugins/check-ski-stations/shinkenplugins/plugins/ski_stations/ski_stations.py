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


from __future__ import unicode_literals, division, print_function

import sys
import codecs
import urllib

import lxml.html

from shinkenplugins.old import BasePlugin
from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


class Plugin(BasePlugin):
    NAME = 'check-ski-stations'
    VERSION = '0.2'
    DESCRIPTION = 'check if ski stations are open'
    AUTHOR = 'vdnguyen'
    EMAIL = 'vanduc.nguyen@savoirfairelinux.com'
    
    ARGS = [('h', 'help', 'display plugin help', False),
            ('v', 'version', 'display plugin version number', False),
            ('w', 'warning', 'Limit to result in a warning state', True),
            ('c', 'critical', 'Limit to result in a critical state', True),
            ('l', 'list', 'the list of regions', False),
            ('r', 'region', 'region to check', True),
            ]
    URL = "http://www.zoneski.com/vivelaneige/tableauqc2014-conditions.php"

    @classmethod
    def _get_data(cls):
        response = urllib.urlopen(cls.URL)
        # Read html
        return response.read()

    @classmethod
    def get_data_list(cls):
        page_source = cls._get_data()
        # Parse html/xml
        root = lxml.html.fromstring(page_source)

        data_list = []

        row_list = root.xpath('//table[@id="conditions-table"]/tbody/tr')
        for row in row_list:
            cells = row.getchildren()
            state = cells[0].text_content()
            name = cells[1].text_content()
            region = cells[2].text_content()
            # split day and night data
            day = cells[4].text_content().split("/")
            night = cells[5].text_content().split("/")
            if day[0] == "-":
                day[0] = 0
            if night[0] == "-":
                night[0] = 0
            tmp_dict = {"state":state, "name":name, "region":region, "day":day, "night":night}
            data_list.append(tmp_dict)

        return data_list

    @classmethod
    def get_region_list(cls):
        data_list = cls.get_data_list()
        region_list = []

        for index in data_list:
            if index["region"] not in region_list:
                region_list.append(index["region"])

        region_list.append(u"Tout le Québec")

        return region_list
    
    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        if "region" not in args:
            self.exit(STATES.UNKNOWN, 'Region argument is missing')

        regions_list = self.get_region_list()

        region = args.get("region").decode("utf8")
        if region not in regions_list:
            self.exit(STATES.UNKNOWN, 'Region %r is unknown.' % region)

        return True, None
    
    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        data_list = self.get_data_list()
        # reset these variables at 0
        number_stations = 0
        number_open_stations = 0
        day_downhill = 0
        day_open = 0
        night_downhill = 0
        night_open = 0
        # use to verify if all stations in region are undetermined
        number_unknown_stations = 0

        region = args.get("region").decode("utf8")
        for index in data_list:
            if index["region"] == region or region == u"Tout le Québec":
                number_stations += 1
                if index["state"] == u"Ouvert":
                    number_open_stations += 1
                    day_downhill += int(index["day"][1])
                    day_open += int(index["day"][0])
                    night_downhill += int(index["night"][1])
                    night_open += int(index["night"][0])
                if index["state"] == u"Indéterminé":
                    number_unknown_stations += 1
        # handle if all stations in region are undetermined
        if number_unknown_stations == number_stations:
            message = "OK: There's not information for this region"
            self.exit(STATES.UNKNOWN, message)
        # calculate the number of stations per region
        # included open and close
        number_stations = number_stations - number_unknown_stations
        p1 = PerfData("open_stations",
                      number_open_stations,
                      unit='stations',
                      crit="0",
                      min_="0",
                      max_=number_stations)
        p2 = PerfData('day_open',
                      day_open,
                      unit='downhills',
                      min_="0",
                      max_=day_downhill)
        p3 = PerfData('night_open',
                      night_open,
                      unit='downhills',
                      min_="0",
                      max_=night_downhill)

        if number_open_stations == 0:
            message = ("CRITICAL: There's %s on %s stations open in %s"
            % (number_open_stations, number_stations, region))
            self.exit(STATES.CRITICAL, message, p1, p2, p3)
        else:
            message = ("OK: There's %s on %s stations open in %s"
            % (number_open_stations, number_stations, region))
            self.exit(STATES.OK, message, p1, p2, p3)


def main(argv=None):
    Plugin(argv)


if __name__ == "__main__":
    main()
