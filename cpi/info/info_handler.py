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
    """ Class used to create metric objects """
    def __init__(self, name, formula, description):
        self.name = name
        self.formula = formula
        self.description = description

    def get_name(self):
        return self.name

    def get_formula(self):
        return self.formula

    def get_description(self):
        return self.description

    def __eq__(self, name):
        """ Object of this class is equal if the name received is equals
        to this class name attribute """
        return self.name == name


class InfoHandler(object):
    """Display information about event or metric (occurrences)."""
    PROCESSOR = core.get_processor()
    EVENTS_LIST = events_reader.EventsReader(PROCESSOR)
    METRICS = metrics_calculator.MetricsCalculator(PROCESSOR)

    def __init__(self):
        event_names = self.EVENTS_LIST.get_events()
        self.events_list = self.__get_events_list(event_names)
        self.metrics_list = self.__get_metrics_list()

    def show_info(self, occurrence_item, all_events_opt, all_metrics_opt,
                  all_opt):
        """ Calls the proper function to display event or metric info

        Parameters:
            occurrence - the event or metric to be displayed.
            all_opt - if should display all ocurrences
            all_events_opt - if should display all events only
            all_metrics_opt - if should display all metrics only
        """
        if all_opt:
            self.__show_all()
            sys.exit(0)

        if all_events_opt:
            self.__show_all_events()
            sys.exit(0)

        if all_metrics_opt:
            self.__show_all_metrics()
            sys.exit(0)

        occurrence = occurrence_item[0]
        if occurrence in self.events_list:
            self.__print_events_info(occurrence)
        elif occurrence in self.metrics_list:
            self.__print_metrics_info(occurrence)
        else:
            print "Event or Metric \"{}\" not found.".format(occurrence)
            sys.exit(1)
        sys.exit(0)

    def __show_all_metrics(self):
        """ Show all metrics supported by CPI """
        for obj in self.metrics_list:
            self.__print_metrics_info(obj.get_name())
            print "\n"

    def __show_all_events(self):
        """ Show all events supported by CPI """
        for event in self.events_list:
            self.__print_events_info(event)
            print "\n"

    def __show_all(self):
        """ Show information of all resources (metrics and events) """
        self.__show_all_events()
        self.__show_all_metrics()

    def __print_events_info(self, occurrence_event):
        """ Print information about events """
        print "    Event Name:\t", occurrence_event
        print "    Type:\tEvent"
        print "    Description:", \
            self.EVENTS_LIST.get_event_description(occurrence_event)
        return 0

    def __print_metrics_info(self, occurrence_metric):
        """ Display information about metric_name if it is in the
           metrics_list."""
        print "    Name:\t", self.get_metric_name(occurrence_metric)
        print "    Type:\tMetric"
        print "    Formula:\t", self.get_metric_formula(occurrence_metric)
        print "    Description:",\
            self.get_metric_description(occurrence_metric)
        return 0

    def __get_events_list(self, event_names):
        """ Create a list of all event_keys."""
        events_list = []
        for array in event_names:
            for event in array:
                events_list.append(event)
        return events_list

    def __get_metrics_list(self):
        """ Return a list of metrics objects """
        metric_list = []
        # Populate the list
        for key in self.METRICS.get_raw_metrics().keys():
            name = self.METRICS.get_raw_metrics()[key]["NAME"]
            formula = self.METRICS.get_raw_metrics()[key]["FORMULA"]
            description = self.METRICS.get_raw_metrics()[key]["DESCRIPTION"]
            metric = Metric(name, formula, description)
            metric_list.append(metric)
        return metric_list

    def __get_object_from_metric_list(self, occurrence_metric):
        """ Load the metric object variable values in obj """
        obj = [x for x in self.metrics_list if x.name == occurrence_metric]
        return obj

    def get_metric_name(self, occurrence_metric):
        """Return metric name"""
        try:
            metric = self.__get_object_from_metric_list(occurrence_metric)[0]
            return metric.get_name()
        except IndexError:
            return None

    def get_metric_formula(self, occurrence_metric):
        """Return metric formula """
        try:
            metric = self.__get_object_from_metric_list(occurrence_metric)[0]
            return metric.get_formula()
        except IndexError:
            return None

    def get_metric_description(self, occurrence_metric):
        """ Return metric description """
        try:
            metric = self.__get_object_from_metric_list(occurrence_metric)[0]
            return metric.get_description()
        except IndexError:
            return None
