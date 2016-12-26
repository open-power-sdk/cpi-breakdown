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
        * Daniel Kreling <dbkreling@br.ibm.com>
"""


from terminaltables import AsciiTable


def create_table(file_names, results_list, sort_opt):
    """ Create a table with comparison two output files """

    if not results_list:
        return 1

    title = "Comparison Table"
    print "\nComparing file_names:"
    print "FILE 1 = %s\nFILE 2 = %s" % (file_names[0], file_names[1])
    print "\nNOTE:\nA raise in number of all events represent a decrease in "\
          "the \nperformance of the application. Therefore, the smallest the "\
          "\npercentage, the better the application performance.\n"

    table_data = [
        ['Event Name', 'File 1', 'File 2', 'Percentage']
    ]

    # If --sort was selected in the command line, sort percentage column from
    # largest to smallest (worst to best)
    if sort_opt:
        iterator = sorted(results_list, key=lambda x: x[3], reverse=True)
    else:
        iterator = results_list

    for entry in iterator:
        # if float, convert to string so to display two decimal points
        if isinstance(entry[3], float):
            entry[3] = str("%.2f" % entry[3])
        table_data.append(entry)

    compare_table = AsciiTable(table_data, title)
    compare_table.justify_columns = {1: 'right', 2: 'right', 3: 'right'}
    print compare_table.table

    return 0
