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

import sys
from cpi import core
from cpi import metrics_calculator


class Comparator(object):
    """ Class responsible for dealing with file comparison """

    def __init__(self, profile_list=None):
        # profile_list is a list of profilings, and each profiling is composed
        # by event|metric : value pair
        self.dict_vals = {}
        self.profile_list = []
        if profile_list is not None:
            self.profile_list = profile_list

    def make_comparison(self, comparison_type, file_names=None):
        """ Make profiles comparison and return a list
        of lists composed by: event_name, init_value, final_value and
        percentage"""
        comparison_list = []
        if file_names is None:
            comparison_list = self.__compare_from_lists(comparison_type)
        else:
            comparison_list = self.__compare_from_files(file_names,
                                                        comparison_type)
        return comparison_list

    def __compare_from_files(self, file_names, comparison_type):
        """ Compare event or metric values from file """
        self.load_profiling_list(file_names, comparison_type)
        self.__create_dict(self.profile_list)
        return self.__compare_(self.dict_vals)

    def __create_dict(self, dict_list):
        """ Create a dictionary as {"events" : (val_file_1, val_file_2), ...}
        """
        try:
            for key in dict_list[0]:
                self.dict_vals[key] = tuple(d[key] for d in dict_list)
        except KeyError:
            sys.stderr.write("Could not create values dictionary."
                             "\nSelect properly formatted files and run the "
                             "compare feature again.\n")
            sys.exit(1)

    def __compare_from_lists(self, comparison_type):
        """ Compare form list of dictionaries """
        if comparison_type == 'metric':
            metrics = {}
            # Calculate metrics values
            processor = core.get_processor()
            metrics_calc = metrics_calculator.MetricsCalculator(processor)
            for events in self.profile_list:
                metrics_values = metrics_calc.calculate_metrics(events)
                for values in metrics_values:
                    metrics[str(values[0])] = values[1]
                self.profile_list.append(metrics)

        self.__create_dict(self.profile_list)
        return self.__compare_(self.dict_vals)

    @classmethod
    def __compare_(cls, dict_vals):
        """ Calculate the percentage from dictionary values and return a list
        of lists composed by: event_name, init_value, final_value and
        percentage"""
        final_array = []
        for key in dict_vals:
            try:
                init_value = float(dict_vals[key][0])
                final_value = float(dict_vals[key][1])
            except ValueError:
                sys.stderr.write("Could not perform the comparison."
                                 "\nSelect properly formatted files and "
                                 "run the compare feature again.\n")
                sys.exit(1)

            if init_value != 0:
                percentage = core.percentage(init_value, final_value)
            elif final_value == 0:
                percentage = float(0.00)
            else:
                percentage = "n/a"

            try:
                percentage = float(percentage)
                # If the number is negative and too small, round to zero
                if percentage == -0.00:
                    percentage = float(0.00)
            except ValueError:
                # Do nothing, the percentage is the "n/a" string
                pass
            final_array.append([key, init_value, final_value, percentage])
        # Sort the list and move the n/a percentages to the end
        final_array = sorted(final_array, key=lambda x:
                             (not isinstance(x[3], str), x[3]),
                             reverse=True)
        return final_array

    def load_profiling_list(self, file_names, comparison_type):
        """ Create a list with two dictionaries containing
        "event|metric:value" pairs """
        dict_list = []
        for file_name in file_names:
            events = core.get_events_from_file(file_name)
            if comparison_type == 'event':
                dict_list.append(events)
            elif comparison_type == 'metric':
                metrics = {}
                # Calculate metrics values
                processor = core.get_processor()
                metrics_calc = metrics_calculator.MetricsCalculator(processor)
                metrics_values = metrics_calc.calculate_metrics(events)
                for values in metrics_values:
                    metrics[str(values[0])] = values[1]
                dict_list.append(metrics)
        self.profile_list = dict_list
