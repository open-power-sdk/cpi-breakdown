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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

from cpi import core


class Comparator:
    """ Class responsible for dealing with file comparison """

    def __init__(self, dict_list):
        # dict_list is a list of dictionaries, and each dictionary is composed
        # by event:value pair
        self.dict_vals = {}
        self.__create_dict(dict_list)

    def __create_dict(self, dict_list):
        """ Create a dictionary as {"events" : (val_file_1, val_file_2), ...}
        """
        try:
            for key in dict_list[0]:
                self.dict_vals[key] = tuple(d[key] for d in dict_list)
        except KeyError:
            raise KeyError

    def compare(self, sort):
        """ Calculate the percentage from dictionary values and return a list
        of lists composed by: event_name, init_value, final_value and
        percentage"""

        final_array = []
        for key in self.dict_vals:
            try:
                init_value = int(self.dict_vals[key][0])
                final_value = int(self.dict_vals[key][1])
            except ValueError:
                raise ValueError

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

        # If should short the final list
        if sort:
            # Sort the list and move the n/a percentages to the end
            final_array = sorted(final_array, key=lambda x:
                                 (not isinstance(x[3], str), x[3]),
                                 reverse=True)
        return final_array
