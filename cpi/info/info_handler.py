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
        * Daniel Kreling <dbkreling@br.ibm.com>
"""
from cpi import core
from cpi import events_reader


events_list = events_reader.EventsReader(core.get_processor())


class InfoHandler(object):
    """Display information of event/metric."""

    def __init__(self, name):
        self.name = name
        self.events_keys = []
        self.event_names = events_list.get_events()

    def show_events_info(self, event_name):
        """ Display information about event if it is in the keys_list """
        keys_list = self.__keys_list()
        if event_name in keys_list:
            print "    Event Name:\n\t", event_name
            print "    Description:\n\t", events_list.get_event_description(event_name)
        else:
            print "Event not found."
            return 1

    def __keys_list(self):
        """ Create a list of all event_keys."""
        for a in self.event_names:
            for e in a:
                self.events_keys.append(e)
        return self.events_keys
