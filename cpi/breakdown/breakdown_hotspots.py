# -*- coding: utf-8 -*-

"""
Copyright (C) 2016 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Roberto Oliveira <rdutra@br.ibm.com>
"""


class HotSpots:
    """ Deals with metrics and events hot spots (higher values) """
    TABULATION = "    "

    def __init__(self, hotspot_value, metrics_list, events_dict):
        self.hotspot_value = hotspot_value
        self.metrics_value = metrics_list
        # Convert to list
        self.events_value = events_dict.items()

    def print_hotspots(self):
        """ Print both events and metrics hot spots """
        self.__print_logo()
        print "Metrics:"
        self.__print_info(self.metrics_value)
        print "\nEvents:"
        self.__print_info(self.events_value)

    def __print_logo(self):
        """ Print the hot spots logo """
        title = "Hot Spots"
        border = "=" * len(title)
        print "\n"
        print border
        print title
        print border

    def __print_info(self, values_list):
        """ Print hot spot information """
        values_list = sorted(values_list, key=lambda x: float(x[1]),
                             reverse=True)

        # Use the 'n' first elements
        values_list = values_list[:self.hotspot_value]

        for element in values_list:
            name = element[0]
            value = element[1]
            print self.TABULATION + name + " : " + str(value)
