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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import unittest

import cpi.drilldown.drilldown_core as drilldown_core
from cpi import core
from cpi import events_reader


class DrilldownCoreTest(unittest.TestCase):
    """ Class to test drilldown core """
    valid_bin = "/bin/sleep"
    invalid_bin = "/bin/foo/bar"
    valid_event = "PM_RUN_CYC"
    invalid_event = "FOO_BAR"
    count = "100000"

    def sort_events_test(self):
        valid_events_dict = {'event1': '100',
                             'event2': '50',
                             'event3': '200',
                             'event4': '80'
                             }
        events = drilldown_core.sort_events(valid_events_dict)
        self.assertEqual("event3", events[0][0])
        self.assertEqual("event1", events[1][0])
        self.assertEqual("event4", events[2][0])
        self.assertEqual("event2", events[3][0])

        invalid_events_dict = {'event1': '100',
                               'event2': '50A',
                               }
        with self.assertRaises(SystemExit) as cm:
            events = drilldown_core.sort_events(invalid_events_dict)
        self.assertEqual(cm.exception.code, 1)

    def run_operf_test(self):
        # Run with valid binary
        drilldown_core.run_operf(self.valid_bin, "1", self.valid_event,
                                 self.count)

        # Run with invalid binary
        with self.assertRaises(SystemExit) as cm:
            drilldown_core.run_operf(self.invalid_bin, "", self.valid_event,
                                     self.count)
        self.assertEqual(cm.exception.code, 1)

    def run_opreport_test(self):
        report_file = "opreport.xml"

        drilldown_core.run_operf(self.valid_bin, "1", self.valid_event,
                                 self.count)
        # Run with valid event
        drilldown_core.run_opreport(self.valid_event, report_file)

        # Run with invalid event
        with self.assertRaises(SystemExit) as cm:
            drilldown_core.run_opreport(self.invalid_event, report_file)
        self.assertEqual(cm.exception.code, 1)
