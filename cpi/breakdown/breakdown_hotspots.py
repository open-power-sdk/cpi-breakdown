# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 IBM Corporation

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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""


class HotSpots(object):
    """ Deals with metrics and events hot spots (higher values) """
    TABULATION = "    "

    def print_metrics_hotspots(self, top_metrics, metrics_list):
        """ Print metrics hot spots """
        if top_metrics <= 0:
            return 0
        self.__print_logo("Metrics")
        self.__print_info(metrics_list, top_metrics)

    def print_events_hotspots(self, top_events, events_list):
        """ Print events hot spots """
        if top_events <= 0:
            return 0
        self.__print_logo("Events")
        self.__print_info(events_list, top_events)

    @staticmethod
    def __print_logo(element_name):
        """ Print the hot spots logo """
        title = element_name + " Hot Spots"
        border = "=" * len(title)
        print ""
        print border
        print title
        print border

    def __print_info(self, values_list, top_value):
        """ Print hot spot information """
        values_list = sorted(values_list, key=lambda x: float(x[1]),
                             reverse=True)

        # Use the 'n' first elements
        values_list = values_list[:top_value]

        for element in values_list:
            name = element[0]
            value = element[1]
            print self.TABULATION + name + " : " + str(value)
