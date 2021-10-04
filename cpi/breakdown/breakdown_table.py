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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

from terminaltables import AsciiTable


class MetricsTable():
    """ Print the CPI Breakdown in table format """

    def __init__(self, metrics_values):
        self.metrics_values = metrics_values

    def print_table(self):
        '''
        Pretty print the table with metric, value and
        percentage
        '''
        met_table = [['Metric', 'Value', 'Percentage']]
        for row in self.metrics_values:
            met_table.append(row)
        met_tab = AsciiTable(met_table)
        met_tab.justify_columns = {1: 'right', 2: 'right'}
        print(met_tab.table)
