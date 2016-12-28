#! /usr/bin/env python
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
        * rafael Peria de Sene <rpsene@br.ibm.com>
"""

import unittest
import os
import parser
import re

from cpi.metrics_calculator import MetricsCalculator

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class MetricsCalculationTests(unittest.TestCase):
    '''
    Test cases for metrics calculation structure
    '''

    metric_pattern = re.compile("(\(?[-+]?[0-9]*\.?[0-9]+[\/\+\-\*]\)?)+")

    def test_eval_add_sub(self):
        '''
        Verify that eval is able to calculate functions
        with precedence
        '''
        equation = str((1 - (1 + 1 + 1 + 1 + 1)))
        self.assertTrue(eval(equation) == -4)
        self.assertFalse(eval(equation) == 4)

    def test_eval_mult(self):
        '''
        Verify that eval is able to calculate functions
        with precedence
        '''
        equation = str((1 - ((2 * 3) - 1) * -1))
        self.assertTrue(eval(equation) == 6)
        self.assertFalse(eval(equation) == -6)

    def test_replace_events_for_value(self):
        '''
        Test the events replacement and calculation
        '''
        equation = '(PM_CMPLU_STALL_THRD - (PM_CMPLU_STALL_LWSYNC + \
        PM_CMPLU_STALL_HWSYNC + PM_CMPLU_STALL_MEM_ECC_DELAY + \
        PM_CMPLU_STALL_FLUSH + PM_CMPLU_STALL_COQ_FULL))'

        parsed_output = {
            'PM_CMPLU_STALL_THRD': '1',
            'PM_CMPLU_STALL_LWSYNC': '1',
            'PM_CMPLU_STALL_HWSYNC': '1',
            'PM_CMPLU_STALL_MEM_ECC_DELAY': '1',
            'PM_CMPLU_STALL_FLUSH': '1',
            'PM_CMPLU_STALL_COQ_FULL': '1'}

        calc_function = re.split("([+-/*/(/)//])", equation.replace(" ", ""))

        for parameter in calc_function:
            if parameter in parsed_output:
                calc_function[calc_function.index(parameter)] = \
                    parsed_output.get(parameter)[0]
        metric = ''.join(calc_function)
        metric_result = eval(metric)
        self.assertTrue(metric_result == -4)
        self.assertTrue(self.metric_pattern.match(str(metric)))

    def test_read_metrics(self):
        """ Test with an invalid file """
        with self.assertRaises(SystemExit) as exit_status:
            metrics = MetricsCalculator("POWER7")
        self.assertEqual(exit_status.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
