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
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

from terminaltables import AsciiTable


class CompareView(object):
    """ Handles the display of the comparison results """

    def __init__(self, results_list, comparison_type, file_names):
        self.results_list = results_list
        self.comparison_type = comparison_type
        self.file_names = file_names

    def create_table(self):
        """ Create a table with comparison two output files """
        title = ""
        print "\nComparing file names:"
        print "File 1 = %s\nFile 2 = %s" % (self.file_names[0],
                                            self.file_names[1])
        print "\nNOTE:\nA raise in number of all elements represent"
        print "a decrease in the performance of the application."
        print "Therefore, the smallest the percentage, the better"
        print "the application performance.\n"

        elem_name = ''
        if self.comparison_type == 'event':
            elem_name = 'Event Name'
            title = "----- Comparison Table for Events"
        elif self.comparison_type == 'metric':
            elem_name = 'Metric Name'
            title = "----- Comparison Table for Metrics"
        table_data = [[elem_name, 'File 1', 'File 2', 'Percentage']]

        for entry in self.results_list:
            # if float, convert to string so to display two decimal points
            if isinstance(entry[3], float):
                entry[3] = str("%.2f" % entry[3])
            table_data.append(entry)

        compare_table = AsciiTable(table_data, title)
        compare_table.justify_columns = {1: 'right', 2: 'right', 3: 'right'}
        print compare_table.table

    def print_csv_format(self):
        """ Print the results in a csv format """
        for element in self.results_list:
            print ','.join(map(str, element))

    def show(self, cvs_format=None):
        """ Show comparison results metrics or events"""
        if cvs_format:
            self.print_csv_format()
        else:
            self.create_table()
