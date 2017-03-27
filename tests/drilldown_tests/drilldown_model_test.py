#! /usr/bin/env python
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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import unittest
import os

from cpi.drilldown.drilldown_model import *


class DrilldownModelTest(unittest.TestCase):
    """ Class to test drilldown model """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_file = dir_path + "/opreport.xml"

    def __init__(self, *args, **kwargs):
        # Create the drilldown model
        model = DrilldownModel()
        self.binmodule_list = model.create_drilldown_model(self.test_file)
        super(DrilldownModelTest, self).__init__(*args, **kwargs)

    def binmodule_test(self):
        expected_binmodules = ["85.3% in /usr/lib64/power8/libc-2.17.so",
                               "14.5% in /home/iplsdk/sync-rhel/main.x",
                               "0.18% in /no-vmlinux",
                               "0.02% in /usr/lib64/ld-2.17.so"]

        assert not [] == self.binmodule_list
        self.assertEquals(4, len(self.binmodule_list))

        # Check if all binmodules matches
        for index, binmodule in enumerate(self.binmodule_list):
            self.assertEqual(expected_binmodules[index],
                             binmodule.get_text())

    def binary_element_test(self):
        expected_symbols = [
            "8.74% in lower [/home/iplsdk/sync-rhel/lowercase.c]",
            "4.51% in create_string [/home/iplsdk/sync-rhel/lowercase.c]",
            "1.25% in 00000037.plt_call.rand@@GLIBC_2.17 [??]"]

        expected_samples = ["3.84% on line 32",
                            "2.5% on line 30",
                            "2.39% on line 31"]

        # Get symbols from the binary element
        symbols_list = self.binmodule_list[1].get_symbols_list()
        self.assertEquals(3, len(symbols_list))

        # Check if all binary symbols matches
        for index, symbol in enumerate(symbols_list):
            self.assertEqual(expected_symbols[index],
                             symbol.get_text())

        # Get samples from first symbol
        samples_list = symbols_list[0].get_samples_list()
        self.assertEquals(3, len(samples_list))

        # Check if all binary samples matches
        for index, samples in enumerate(samples_list):
            self.assertEqual(expected_samples[index],
                             samples.get_text())

    def module_elements_test(self):
        expected_symbols = [
            "77.58% in random [??]",
            "4.83% in random_r [??]",
            "2.71% in rand [??]",
            "0.15% in __strlen_power7 [??]",
            "< 0.01% in _IO_file_write@@GLIBC_2.17 [??]",
            "< 0.01% in __mpn_mul_1 [??]",
            "< 0.01% in __printf_fp@@GLIBC_2.17 [??]",
            "< 0.01% in _dl_addr [??]",
            "< 0.01% in generic_start_main.isra.0 [??]"]

        # Get symbols from the module element
        symbols_list = self.binmodule_list[0].get_symbols_list()
        self.assertEquals(9, len(symbols_list))

        # Check if all modules symbols matches
        for index, symbol in enumerate(symbols_list):
            self.assertEqual(expected_symbols[index], symbol.get_text())

        # No samples available
        for symbol in symbols_list:
            self.assertEquals([], symbol.get_samples_list())


if __name__ == '__main__':
    unittest.main()
