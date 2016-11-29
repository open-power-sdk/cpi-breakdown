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
        * Rafael Sene <rpsene@br.ibm.com>
        * Daniel Kreling <dbkreling@br.ibm.com>
"""

import unittest
import platform
import commands
from cpi import core


class TestCmdExecution(unittest.TestCase):
    def test_cmdexec(self):
        self.assertEqual(0, core.execute("ls"))


class TestCmdExist(unittest.TestCase):
    @staticmethod
    def test_cmdexist():
        assert True == core.cmdexists("cd")


class TestPlatform(unittest.TestCase):
    def test_platform(self):
        self.assertEqual('Linux', platform.system())


class TestProcessor(unittest.TestCase):
    def test_processor(self):
        self.assertEqual(commands.getoutput("grep -io 'power[[:digit:]]\+' -m 1 /proc/cpuinfo"),
                         core.get_processor())

if __name__ == '__main__':
    tests = [TestCmdExecution, TestCmdExist, TestPlatform, TestProcessor]
    loader = unittest.TestLoader()
    test_suit = []

    for test in tests:
        suite = loader.loadTestsFromTestCase(test)
        test_suit.append(suite)

    big_suite = unittest.TestSuite(test_suit)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
