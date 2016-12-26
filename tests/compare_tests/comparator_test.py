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
"""

import unittest

from cpi.compare.comparator import Comparator


class ComparatorTests(unittest.TestCase):
    """ Class to run tests from comparator """

    # Correct dict_list
    dict_list1 = [{"event1": "100", "event2": "200"},
                  {"event1": "200", "event2": "400"}]

    # event1 is different from event10 in second dictionary
    dict_list2 = [{"event1": "100", "event2": "200"},
                  {"event10": "200", "event2": "400"}]

    # event2 has an invalid value number
    dict_list3 = [{"event1": "100", "event2": "200A"},
                  {"event1": "200", "event2": "400"}]

    def test_create_dict(self):
        comparator = Comparator(self.dict_list1)

        with self.assertRaises(KeyError):
            comparator = Comparator(self.dict_list2)

    def test_comparison(self):
        comparator = Comparator(self.dict_list1)
        list1 = comparator.compare()
        self.assertEqual(2, len(list1))

        # Get first internal list
        l = list1[0]
        self.assertEqual(4, len(l))
        self.assertEqual("event2", l[0])
        self.assertEqual(200, l[1])
        self.assertEqual(400, l[2])
        self.assertEqual(100.00, l[3])

        with self.assertRaises(ValueError):
            comparator = Comparator(self.dict_list3)
            comparator.compare()

if __name__ == '__main__':
    unittest.main()
