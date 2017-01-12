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
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import unittest

from cpi.compare.comparator import Comparator


class ComparatorTests(unittest.TestCase):
    """ Class to run tests from comparator """

    # Correct dict_list
    dict_list1 = [{"event1": "100", "event2": "300",
                   "event3": "100", "event4": "0"},
                  {"event1": "200", "event2": "400",
                   "event3": "1000", "event4": "10"}]

    # event1 is different from event10 in second dictionary
    dict_list2 = [{"event1": "100", "event2": "200"},
                  {"event10": "200", "event2": "400"}]

    # event2 has an invalid value number
    dict_list3 = [{"event1": "100", "event2": "200A"},
                  {"event1": "200", "event2": "400"}]

    def test_create_dict(self):
        comparator = Comparator(self.dict_list1)

    def test_compare(self):
        comparator = Comparator(self.dict_list1)

        # Test events
        print "test len(self.dict_list1):" + str(len(self.dict_list1))
        list1 = comparator.make_comparison('event')
        print "test len(list1):" + str(len(list1))
        self.assertEqual(4, len(list1))
        # Get first internal list
        l = list1[0]
        self.assertEqual(4, len(l))
        self.assertEqual("event3", l[0])
        self.assertEqual(100, l[1])
        self.assertEqual(1000, l[2])
        self.assertEqual(900, l[3])
        # Get second internal list
        l = list1[1]
        self.assertEqual(4, len(l))
        self.assertEqual("event1", l[0])
        self.assertEqual(100, l[1])
        self.assertEqual(200, l[2])
        self.assertEqual(100, l[3])

if __name__ == '__main__':
    unittest.main()
