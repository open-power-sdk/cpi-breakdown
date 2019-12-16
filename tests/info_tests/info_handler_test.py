#! /usr/bin/env python3
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
        * Daniel Kreling <dbkreling@br.ibm.com>
"""
import unittest
from cpi.info.info_handler import InfoHandler


class InfoHandlerTest(unittest.TestCase):
    '''
    Test cases for InfoHandler
    '''
    VALID_METRIC = ["RUN_CPI"]
    INVALID_METRIC = ["FOO_BAR"]
    DESCRIPTION = "Run cycles per run instruction"
    FORMULA = "PM_RUN_CYC / PM_RUN_INST_CMPL"

    ih = InfoHandler()

    def show_info_test(self):
        """ Test show_info method """
        with self.assertRaises(SystemExit) as cm:
            self.ih.show_info(self.VALID_METRIC, False, False, False)
        self.assertEqual(cm.exception.code, 0)

        with self.assertRaises(SystemExit) as cm:
            self.ih.show_info(self.INVALID_METRIC, False, False, False)
        self.assertEqual(cm.exception.code, 1)

    def show_all_events_test(self):
        """ Test show_all_events method """
        with self.assertRaises(SystemExit) as cm:
            self.ih.show_info(self.VALID_METRIC, True, False, True)
        self.assertEqual(cm.exception.code, 0)

    def show_all_metrics_test(self):
        """ Test show_all_metrics method """
        with self.assertRaises(SystemExit) as cm:
            self.ih.show_info(self.VALID_METRIC, False, True, True)
        self.assertEqual(cm.exception.code, 0)

    def show_all_test(self):
        """ Test show_all method """
        with self.assertRaises(SystemExit) as cm:
            self.ih.show_info(self.VALID_METRIC, False, False, True)
        self.assertEqual(cm.exception.code, 0)

    def get_metric_name_test(self):
        """ Test if correctly displaying metric name """
        self.assertEqual(self.VALID_METRIC[0],
                          self.ih.get_metric_name(self.VALID_METRIC[0]))
        self.assertEqual(None,
                          self.ih.get_metric_name(self.INVALID_METRIC[0]))

    def get_metric_formula_test(self):
        """ Test if correctly displaying metric formula """
        self.assertEqual(self.FORMULA,
                          self.ih.get_metric_formula(self.VALID_METRIC[0]))
        self.assertEqual(None,
                          self.ih.get_metric_formula(self.INVALID_METRIC[0]))

    def get_metric_description_test(self):
        """ Test if correctly displaying metric description """
        self.assertEqual(self.DESCRIPTION,
                          self.ih.get_metric_description(self.VALID_METRIC[0]))
        self.assertEqual(None,
                          self.ih.get_metric_description(self.INVALID_METRIC[0]
                                                         ))


if __name__ == '__main__':
    unittest.main()
