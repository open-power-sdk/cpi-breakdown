# -*- coding: utf-8 -*-

"""
Copyright (C) 2017,2019 IBM Corporation

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
        * Rafael Peria Sene <rpsene@br.ibm.com>
        * Matheus Castanho <mscastanho@ibm.com>
"""

import os
import re
import sys
from collections import defaultdict
from math import fabs
import yaml

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class MetricsCalculator():
    '''
    Class that calculates metrics
    '''
    metrics_groups = []

    def __init__(self, processor):
        metrics_file = DIR_PATH + "/metrics/" + str.lower(processor) + ".yaml"
        self.metrics_groups = self.__read_metrics(metrics_file)

    @staticmethod
    def __read_metrics(metrics_file):
        """ Get the metrics based on the processor version. They are located
        at /metrics/<processor_model>.yaml. It returns a dictionary which
        contains the NAME an the EQUATION """
        try:
            with open(metrics_file, "r") as metrics:
                return yaml.load(metrics, Loader=yaml.FullLoader)
        except IOError:
            sys.stderr.write("Could not find file '{}'. Check if your "
                             "installation is correct or try to install "
                             "cpi again.\n".format(metrics_file))
            sys.exit(1)

    def get_raw_metrics(self):
        '''Return the raw metrics collect from its file'''
        return self.metrics_groups

    def calculate_metrics(self, parsed_output_dict):
        '''
        Calculate the metrics based on the processor model and returns a list
        of list which contains:
                [
                [METRIC_NAME_1, METRIC_RESULT_1, METRIC_PERCENT_1],
                [METRIC_NAME_2, METRIC_RESULT_2, METRIC_PERCENT_2],
                ...
                ]
        It receives a dictonary with the parsed output of the execution.
        This dict content is <EVENT> : <VALUE> like:
            PM_CMPLU_STALL_THRD : 55322
            PM_CMPLU_STALL_BRU_CRU : 25701
            PM_CMPLU_STALL_COQ_FULL : 178
            PM_CMPLU_STALL_BRU : 16138
        '''
        parsed_output = defaultdict(list)
        parsed_output = parsed_output_dict
        cycles = 'PM_CYC'
        instructions = 'PM_RUN_INST_CMPL'
        if 'PM_CYC' not in parsed_output:
            cycles = 'PM_RUN_CYC'
        metrics_results = []
        if True:
            for group in self.metrics_groups.values():
                result_tmp = []
                # Split the metrics in all components to allow replacing
                # the events with the calculated values.
                # For example, the metric:
                # PM_CMPLU_STALL_DMISS_L3MISS - (PM_CMPLU_STALL_DMISS_LMEM + \
                # PM_CMPLU_STALL_DMISS_L21_L31 + PM_CMPLU_STALL_DMISS_REMOTE)
                # Becomes:
                # [PM_CMPLU_STALL_DMISS_L3MISS, -, (, PM_CMPLU_STALL_DMISS_LMEM,\
                # +, PM_CMPLU_STALL_DMISS_L21_L31, +, \
                # PM_CMPLU_STALL_DMISS_REMOTE, )]
                calc_function = re.split("([+-/*/(/)//])",
                                         group['FORMULA'].replace(" ", ""))
                for parameter in calc_function:
                    # If we find the event in the parsed output, it is
                    # replaced by its value.
                    if parameter in parsed_output:
                        prm = 'float(' + parsed_output.get(parameter) + ')'
                        calc_function[calc_function.index(parameter)] = prm
                # Once the events are replaced by its values in the metric,
                # we put it all togheter again and calculate the metric
                metric = ''.join(calc_function)
                metric_result = eval(metric)
                result_tmp.append(group["NAME"])
                if metric_result > 0:
                    result_tmp.append("%.3f" % metric_result)
                    cmd = ('(float(metric_result)/(float(parsed_output.get'
                           '(cycles))/float(parsed_output.get'
                           '(instructions))))*100')
                    result_tmp.append("%.2f" % eval(cmd))
                else:
                    result_tmp.append(0)
                    result_tmp.append(fabs(0))
                metrics_results.append(result_tmp)
            return metrics_results
        else:
            sys.stderr.write("PM_RUN_INST_CMPL is 0.")
            sys.stderr.write("As it is the base divisor for all metrics \
                             calculation it can not be 0. \
                             Please run CPI again.")
            sys.exit(1)
