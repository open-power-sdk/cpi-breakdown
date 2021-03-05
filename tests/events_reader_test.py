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
        * Daniel Kreling <dbkreling@br.ibm.com>
"""

import unittest
import sys
from cpi import events_reader


VALID_EVENT = "PM_RUN_CYC"
INVALID_EVENT = "FOO_BAR"
PROCESSOR_VERSION = "POWER8"
DESCRIPTION = "Run Cycles. Processor Cycles gated by the run latch. Operating \
systems use the run latch to indicate when they are doing useful work. The \
run latch is typically cleared in the OS idle loop. Gating by the run latch \
filters out the idle loop."


class EventsReaderTests(unittest.TestCase):
    """ Class to run tests from events_reader """
    reader = events_reader.EventsReader(PROCESSOR_VERSION)

    def test_get_events(self):
        events_list = self.reader.get_events()
        assert events_list is not None
        self.assertEqual(20, len(events_list))

    def test_valid_event(self):
        assert self.reader.valid_event(VALID_EVENT) is True
        assert self.reader.valid_event(INVALID_EVENT) is False

    def test_get_event_mincount(self):
        self.assertEqual(100000, self.reader.get_event_mincount(VALID_EVENT))
        self.assertEqual(None, self.reader.get_event_mincount(INVALID_EVENT))

    def test_get_event_description(self):
        self.assertEqual(DESCRIPTION,
                          self.reader.get_event_description(VALID_EVENT))
        self.assertEqual(None, self.reader.get_event_description(INVALID_EVENT))

    def test_read_events(self):
        """ Test with an invalid file """
        with self.assertRaises(SystemExit) as exit_status:
            reader = events_reader.EventsReader("POWER7")
        self.assertEqual(exit_status.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
