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
        * Rafael Sene <rpsene@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

from terminaltables import AsciiTable


class MetricsTable(object):
    """ Print the CPI Breakdown in table format """

    def __init__(self, metrics_values):
        self.metrics_values = metrics_values

    def print_table(self):
        met_table = [['Metric', 'Value', 'Percentage']]
        for row in self.metrics_values:
            met_table.append(row)
        met_tab = AsciiTable(met_table)
        met_tab.justify_columns = {1: 'right', 2: 'right'}
        print met_tab.table


class EventsTable(object):
    """ Print the events values in table format """

    def __init__(self, events_values_dict):
        self.events_values_dict = events_values_dict

    def print_table(self):
        title = "Events Values"
        event_table = [['Event', 'Value']]

        events_values = self.events_values_dict.items()
        for row in events_values:
            event_table.append(row)
        e_table = AsciiTable(event_table, title)
        e_table.justify_columns = {1: 'right'}
        print "\n"
        print e_table.table
