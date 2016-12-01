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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

import unittest
import os

from cpi import core


class DrilldownExecutionTest(unittest.TestCase):
    """ Class to test drilldown execution """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open("./cpi/events/power8.yaml") as f:
        clean_output = []
        events_list = f.read().replace(" ", "").splitlines()
        for event in events_list:
            if 'PM' in event:
                clean_output.append(event.split(':')[0])

    def execution_test(self):
        self.assertTrue(len(self.clean_output) == 45)
        if core.cmdexists('cpi'):
            for event in self.clean_output:
                core.execute('cpi --drilldown=' + event + " sleep 1")


if __name__ == '__main__':
    if "POWER8" in core.get_processor():
        unittest.main()
