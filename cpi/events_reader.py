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
import sys


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class EventsReader:
    """Class to deal with events from yaml files"""

    # Hold events from yaml files
    events = []

    def __init__(self, processor):
        events_file = DIR_PATH + "/events/" + str.lower(processor) + ".yaml"
        self.events = self.__read_events(events_file)

    def get_events(self):
        """Return the events based on the processor version"""
        events_list = []
        for events_dic in self.events:
            # Append dict keys (event name) in list
            events_list.append(events_dic.keys())
        return events_list

    def valid_event(self, event_name):
        """Return if the event is supported in the drilldown"""
        for events_dic in self.events:
            if event_name in events_dic:
                return True
        return False

    def __get_event_dict_value(self, event_name):
        """Return the value (a list) for the event_name key"""
        for events_dic in self.events:
            if event_name in events_dic:
                return events_dic.get(event_name)

    def get_event_mincount(self, event_name):
        """Return the event minimum count"""
        try:
            return self.__get_event_dict_value(event_name)[0]
        except TypeError:
            return None

    def get_event_description(self, event_name):
        """Return the event description"""
        try:
            return self.__get_event_dict_value(event_name)[1]
        except TypeError:
            return None

    def __read_events(self, events_file):
        """Read the events from the respective file"""
        try:
            with open(events_file, "r") as f:
                groups = yaml.load(f)
                events_dic = []
                for i in groups.values():
                    events_dic.append(i)
                return events_dic
        except IOError:
            sys.stderr.write("Could not find file '{}'. Check if your "
                             "installation is correct or try to install "
                             "cpi again.\n".format(events_file))
            sys.exit(1)
