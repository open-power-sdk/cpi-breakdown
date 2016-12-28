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
import sys
from cpi import core
from cpi import events_reader
from cpi import metrics_calculator


class Metric(object):
    """ Create an metric object containing name, formula, components, and
        description"""
    def __init__(self, name, formula, components, description):
        self.name = name
        self.formula = formula
        self.components = components
        self.description = description

    def get_name(self):
        return self.name

    def get_formula(self):
        return self.formula

    def get_components(self):
        return self.components

    def get_description(self):
        return self.description


class InfoHandler(object):
    """Display information about event or metric (occurrences)."""
    PROCESSOR = core.get_processor()
    EVENTS_LIST = events_reader.EventsReader(PROCESSOR)
    METRICS = metrics_calculator.MetricsCalculator(PROCESSOR)

    def __init__(self):
        self.events_keys = []
        self.metrics_keys = []
        self.event_names = self.EVENTS_LIST.get_events()
        self.mo_list = []
        self.__load_metrics()

    def show_info(self, occurrence):
        """ Calls the proper function to display event or metric info """
        # Load events names in a list (self.events_keys).
        self.events_keys = self.__load_events()
        # The same for metric objects (self.mo_list).
        self.mo_list = self.__load_metrics()

        if occurrence in self.events_keys:
            self.__print_events_info(occurrence)
        elif occurrence in self.metrics_keys:
            self.__print_metrics_info(occurrence)
        else:
            print "Event or Metric \"{}\" not found.".format(occurrence)
            sys.exit(1)
        sys.exit(0)

    def __load_events(self):
        """ Return events keys (names) in a list"""
        # Load events names in a list (self.events_keys).
        return self.__events_keys_list()

    def __load_metrics(self):
        """ Return metric objects in a list (self.mo_list) """
        return self.__get_metrics_list()

    def __print_events_info(self, occurrence_event):
        """ Print information about events """
        print "    Type:\n\tEvent"
        print "    Event Name:\n\t", occurrence_event
        print "    Description:\n\t", \
            self.EVENTS_LIST.get_event_description(occurrence_event)
        return 0

    def __print_metrics_info(self, occurrence_metric):
        """ Display information about metric_name if it is in the
           metrics_list."""
        print "    Type:\n\tMetric"
        print "    Metric Name:\n\t", self.get_metric_name(occurrence_metric)
        print "    Formula:\n\t", self.get_metric_formula(occurrence_metric)
        print "    Components:\n\t",\
            self.get_metric_components(occurrence_metric)
        print "    Description:\n\t",\
            self.get_metric_description(occurrence_metric)
        return 0

    def __events_keys_list(self):
        """ Create a list of all event_keys."""
        for array in self.event_names:
            for event in array:
                self.events_keys.append(event)
        return self.events_keys

    def __get_metrics_list(self):
        """ Return a list of objects (self.mo_list) with all metric
            information (keys) """
        # Populate the list
        for key in self.METRICS.get_raw_metrics().keys():
            # set metrics instance variables:
            name = self.METRICS.get_raw_metrics()[key]["NAME"]
            formula = self.METRICS.get_raw_metrics()[key]["FORMULA"]
            components = self.METRICS.get_raw_metrics()[key]["COMPONENTS"]
            description = self.METRICS.get_raw_metrics()[key]["DESCRIPTION"]
            mo = Metric(name, formula, components, description)
            self.metrics_keys.append(name)
            # append mo instance to the instance list
            self.mo_list.append(mo)
        return self.mo_list

    def __get_object_from_mo_list(self, occurrence_metric):
        """ Load the metric object variable values in obj """
        obj = [x for x in self.mo_list if x.name == occurrence_metric]
        return obj

    def get_metric_name(self, occurrence_metric):
        """Return metric name"""
        try:
            metric = self.__get_object_from_mo_list(occurrence_metric)[0]
            return metric.get_name()
        except IndexError:
            return None

    def get_metric_formula(self, occurrence_metric):
        """Return metric formula """
        try:
            metric = self.__get_object_from_mo_list(occurrence_metric)[0]
            return metric.get_formula()
        except IndexError:
            return None

    def get_metric_components(self, occurrence_metric):
        """ Return metric components """
        try:
            metric = self.__get_object_from_mo_list(occurrence_metric)[0]
            if metric.get_components():
                return ", ".join(metric.get_components())
            else:
                return "N/A"
        except IndexError:
            return None

    def get_metric_description(self, occurrence_metric):
        """ Return metric description """
        try:
            metric = self.__get_object_from_mo_list(occurrence_metric)[0]
            return metric.get_description()
        except IndexError:
            return None
