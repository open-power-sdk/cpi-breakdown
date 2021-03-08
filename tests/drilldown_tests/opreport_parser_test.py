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

from cpi.drilldown.opreport_model import *
from cpi.drilldown.opreport_parser import *


class OpreportParserTest(unittest.TestCase):
    """ Class to test opreport parser and model """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_file = dir_path + "/opreport.xml"

    def parse_test(self):
        parser = OpreportParser()
        binmodule_list = parser.parse(self.test_file)
        assert not [] == binmodule_list
        self.assertEqual(4, len(binmodule_list))

        # First module element
        module = binmodule_list[0]
        self.assertEqual("/usr/lib64/ld-2.17.so", module.get_name())
        self.assertEqual(4, module.get_count())
        self.assertEqual(2, len(module.get_symbol_list()))

        # The Binary element
        binary = binmodule_list[-1]
        self.assertEqual("/home/iplsdk/sync-rhel/main.x", binary.get_name())
        self.assertEqual(3167, binary.get_count())
        self.assertEqual(3, len(binary.get_symbol_list()))

        # Last binary symbol
        symbol = binary.get_symbol_list()[-1]
        self.assertEqual("2", symbol.get_idref())
        self.assertEqual(272, symbol.get_count())

        # Fist binary symbol
        symbol = binary.get_symbol_list()[0]
        self.assertEqual("0", symbol.get_idref())
        self.assertEqual(1910, symbol.get_count())

        # Symbol data of first binary symbol
        symboldata = symbol.get_symboldata()
        self.assertEqual("0", symboldata.get_id())
        self.assertEqual("lower", symboldata.get_name())
        self.assertEqual("/home/iplsdk/sync-rhel/lowercase.c",
                         symboldata.get_file_name())
        self.assertEqual("28", symboldata.get_line())

        # Symbol details
        symboldetails = symboldata.get_symboldetails()
        self.assertEqual("0", symboldetails.get_id())
        self.assertEqual(3, len(symboldetails.get_detaildata_list()))

        # First detail data
        detaildata = symboldetails.get_detaildata_list()[0]
        self.assertEqual("31", detaildata.get_line())
        self.assertEqual(523, detaildata.get_count())

        # Last detail data
        detaildata = symboldetails.get_detaildata_list()[-1]
        self.assertEqual("30", detaildata.get_line())
        self.assertEqual(547, detaildata.get_count())


if __name__ == '__main__':
    unittest.main()
