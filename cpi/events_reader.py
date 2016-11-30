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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import yaml
import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class EventsReader:
    """Class to deal with events from yaml files"""
    processor_version = ''

    # Hold events from yaml files
    events = []

    def __init__(self, processor_version):
        self.processor_version = processor_version
        events_file = DIR_PATH + "/events/" + str.lower(processor_version) + ".yaml"
        self.events = self.read_events(events_file)

    def get_events(self):
        """return the events based on the processor version"""
        events_list = []
        for events_dic in self.events:
            # Append dict keys (event name) in list
            events_list.append(events_dic.keys())
        return events_list

    def get_event_mincount(self, event_name):
        """Return the event minimum count"""
        # TODO: Implement me in next patch

    def read_events(self, events_file):
        """
        Read the events from the respective file.
        PS: Not intented to be used outside this class
        """
        with open(events_file, "r") as f:
            groups = yaml.load(f)
            events_dic = []
            for i in groups.values():
                events_dic.append(i)
            return events_dic
