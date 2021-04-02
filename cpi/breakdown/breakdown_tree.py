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
"""


class BreakdownTree(object):
    '''
    Print the CPI Breakdown Tree using as predefined model according the
    processor where the application is running.
    '''
    metrics_value_dict = {}
    metric_components = {}
    IDENTATION = '      '

    def __init__(self, metrics, metrics_calculation):
        # Convert the list with the calculated metric values to a dict
        for metric_calc in metrics_calculation:
            self.metrics_value_dict[metric_calc[0]] = str(metric_calc[1]) + \
             ' (' + str(metric_calc[2]) + ' %)'

        # Get all breakdown components
        for group in metrics.values():
            if group['COMPONENTS']:
                group_name = str(group['NAME'])
                self.metric_components[group_name] = group['COMPONENTS']

    def print_tree(self):
        '''
        Starts the printing process by the first level on events which
        contains RUN_CPI
        '''
        identation_size = 1
        print()
        print("RUN_CPI" + ': ' + self.metrics_value_dict["RUN_CPI"])
        level1 = self.metric_components['RUN_CPI']
        for level2 in level1:
            msg = self.IDENTATION + level2 + ': '
            print(msg + self.metrics_value_dict[level2])
            self.print_level(level2, identation_size)

    def print_level(self, current_level, identation):
        '''
        Iterate recursively in all breakdown components printing what is
        available in each level
        '''
        if current_level in self.metric_components:
            identation += 2
            for next_level in self.metric_components[current_level]:
                print(self.IDENTATION * identation + next_level + \
                 ': ' + self.metrics_value_dict[next_level])
                self.print_level(next_level, identation)
