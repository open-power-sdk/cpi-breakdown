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
        * Rafael Sene <rpsene@br.ibm.com>
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import unittest
import csv
from cpi import core


class CoreTests(unittest.TestCase):
    """ Class to run tests from core """

    def test_execute(self):
        self.assertEqual(0, core.execute("cd"))
        self.assertNotEqual(0, core.execute("foo_bar"))

    def test_execute_stdout(self):
        status, output = core.execute_stdout("cd")
        self.assertEqual(0, status)
        self.assertEqual("", output)

        status, output = core.execute_stdout("ls /bla/foo")
        self.assertNotEqual(0, status)
        self.assertIn(b"No such file or directory", output)

    def test_cmdexist(self):
        assert core.cmdexists("cd") is True
        assert core.cmdexists("foo_bar") is False

    def test_get_processor(self):
        self.assertEqual("POWER8", core.get_processor())

    def test_supported_processor(self):
        assert core.supported_processor("POWER7") is False
        assert core.supported_processor("POWER8") is True

    def test_percentage(self):
        self.assertEqual("100.00", core.percentage(10, 20))
        self.assertEqual("-50.00", core.percentage(20, 10))
        self.assertEqual("0.00", core.percentage(10, 10))


if __name__ == '__main__':
    unittest.main()
