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

import yaml
import os

def get_events(processor):
    """return the events based on the processor version"""
    events_file = os.path.abspath("../events/" + str.lower(processor) + ".yaml")
    return read_events(events_file)


def read_events(events_file):
    """read the events from the respective file"""
    with open(events_file, "r") as f:
        groups = yaml.load(f)
        events_list = []
        for i in groups.values():
            events_list.append(i)
        return events_list
