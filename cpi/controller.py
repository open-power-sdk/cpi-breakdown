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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import os
import sys
import time

import core
import events_reader
import metrics_calculator
from info.info_handler import InfoHandler
from breakdown.breakdown_tree import BreakdownTree
from breakdown.breakdown_table import MetricsTable
from breakdown.breakdown_hotspots import HotSpots
from drilldown.drilldown_view import DrilldownView
import drilldown.drilldown_core as drilldown_core
from compare.compare_view import CompareView
from compare.comparator import Comparator


class Controller(object):
    """
    Controls the execution of CPI commands
    """
    def __init__(self):
        self.__binary_path = ''
        self.__binary_args = ''

    def run(self, args):
        """
        Executes the correct action according the user input.

        Parameters:
            args - arguments collected by argparser
        """
        try:
            self.__binary_path = args.cmd[0]
        except (IndexError, AttributeError):
            self.__binary_path = ''
        try:
            self.__binary_args = ' '.join(("'" + i + "'")
                                          for i in args.cmd_args)
        except (IndexError, AttributeError):
            self.__binary_args = ''

        # Run display
        if 'display_file' in args:
            self.__display(args.display_file, args.breakdown_format,
                           args.top_events, args.top_metrics)
        # Run compare
        elif 'cpi_files' in args:
            self.__run_compare(args.type_opt, args.cpi_files, args.csv)
        # Run drilldown
        elif 'event_name' in args:
            self.__run_drilldown(args.event_name)
        # Run info
        elif 'occurrence_info' in args:
            self.__show_info(args.occurrence_info, args.all_events_opt,
                             args.all_metrics_opt, args.all_opt)
        # Run recorder
        else:
            self.__record(args.output_file, args.quiet)

    def __record(self, cpi_file_name, quiet=False):
        """ Record the events and their values in a .cpi file

        Parameters:
            cpi_file_name - the path where the cpi file will be generated
            quiet - if should suppress any message during the recording step
        """
        ocount = "ocount"
        core.supported_feature(core.get_processor(), "Breakdown")
        if not os.path.isfile(self.__binary_path):
            sys.stderr.write(self.__binary_path + ' binary file not found\n')
            sys.exit(1)

        timestamp = core.get_timestamp()
        binary_name = self.__binary_path.split("/").pop(-1)
        dir_current = os.getcwd()
        ocount_out = dir_current + "/output"

        if not core.cmdexists(ocount):
            sys.stderr.write(ocount + " is not installed in the system. " +
                             "Install oprofile before continue." + "\n")
            sys.exit(2)

        reader = events_reader.EventsReader(core.get_processor())

        if not cpi_file_name:
            cpi_file_name = dir_current + "/" + binary_name + "_" + timestamp + ".cpi"
        else:
            dir_file = os.path.dirname(os.path.realpath(cpi_file_name))
            if not os.path.exists(dir_file):
                sys.stderr.write(dir_file +  " directory not found\n")
                return 1
            elif os.path.isdir(cpi_file_name):
                sys.stderr.write(cpi_file_name +  " is not a file\n")
                return 1

        start_time = time.time()
        exec_counter = 0
        events = {}

        # Run ocount for all events groups
        for event in reader.get_events():
            exec_counter = exec_counter + 1
            ocount_cmd = ocount + " -b -f " + ocount_out
            for item in event:
                ocount_cmd += " -e " + item
            if not quiet:
                sys.stdout.write("\r    Recording CPI Events: %d/%d "
                                 "iterations (elapsed time: %d seconds)"
                                 % (exec_counter, len(reader.get_events()),
                                    (time.time() - start_time)))
                sys.stdout.flush()
            status, output = core.execute_stdout(ocount_cmd + ' ' +
                                                 self.__binary_path + ' ' +
                                                 self.__binary_args)
            if status != 0:
                sys.stderr.write("\n\nFailed to run {0} command.".
                                 format(ocount) + "\n" + output + "\n")
                sys.exit(1)
            core.parse_file(ocount_out, events)
        core.execute("rm " + ocount_out)
        if not quiet:
            print ""

        core.save_events(events, cpi_file_name)
        return events

    @classmethod
    def __display(cls, cpi_file, breakdown_format, top_events, top_metrics):
        """
        Show the output of CPI recording

        Parameters:
            cpi_file - the file where the value of the recorded events is saved
            breakdown_format - the format the breakdown output will be printed
            top_events - show top 'n' events
            top_metrics - show top 'n' metrics
        """
        events = core.get_events_from_file(cpi_file)

        # Calculate metrics values
        metrics_calc = metrics_calculator.MetricsCalculator(core.get_processor())
        metrics_value = metrics_calc.calculate_metrics(events)

        # Show events and metrics hot spots
        if top_metrics is not None or top_events is not None:
            hot_s = HotSpots()
            if top_metrics:
                hot_s.print_metrics_hotspots(top_metrics, metrics_value)
            if top_events:
                hot_s.print_events_hotspots(top_events, events.items())
        # Show breakdown output
        else:
            if breakdown_format == 'table':
                sorted_metrics = sorted(metrics_value,
                                        key=lambda x:
                                        float(x[2]),
                                        reverse=True)
                table = MetricsTable(sorted_metrics)
                table.print_table()
            elif breakdown_format == 'tree':
                tree = BreakdownTree(metrics_calc.get_raw_metrics(),
                                     metrics_value)
                tree.print_tree()

    def __run_drilldown(self, event):
        """ Run the drilldown feature

        Parameters:
            event - the event to be used in drilldown
        """
        core.supported_feature(core.get_processor(), "Drilldown")

        if not os.path.isfile(self.__binary_path):
            sys.stderr.write(self.__binary_path + ' binary file not found\n')
            sys.exit(1)

        operf = drilldown_core.OPERF
        if not core.cmdexists(operf):
            sys.stderr.write(operf + " is not installed in the system. " +
                             "Install oprofile before continue." + "\n")
            sys.exit(2)

        events = {event: '0'}
        events = drilldown_core.sort_events(events)
        reader = events_reader.EventsReader(processor)
        # Run drilldown with chosen events
        for element in events:
            event = element[0]
            # Event is not supported with drilldown feature
            if not reader.valid_event(event):
                sys.stderr.write("Event {0} is not supported by drilldown "
                                 "feature.".format(event) +
                                 "\nChoose a supported event and try again\n")
                sys.exit(1)

            sys.stdout.write("\r    Running drilldown with event: %s \n"
                             % (event))

            # Run operf
            min_count = str(reader.get_event_mincount(event))
            drilldown_core.run_operf(self.__binary_path, self.__binary_args,
                                     event, min_count)
            # Run opreport
            report_file = "opreport.xml"
            drilldown_core.run_opreport(event, report_file)

            # Run drilldown
            drilldown_view = DrilldownView()
            drilldown_view.print_drilldown(event, report_file, threshold)

    @classmethod
    def __run_compare(cls, comparison_type, file_names, format_type):
        """ Get the contents of two ocount output files, compare their results
        and display in a table

        Parameters:
            file_names - cpi formatted file names
            comparison_type - choose between event or metric
            csv_format - if should display the result in a csv format
        """

        if comparison_type == 'metric' and  not core.check_supported_feat("Compare metrics"):
            sys.exit(1)

        comparator = Comparator()
        final_array = comparator.make_comparison(comparison_type, file_names)
        compare_view = CompareView(final_array, comparison_type, file_names)
        compare_view.show(format_type)

    @classmethod
    def __show_info(cls, occurrence, all_events_opt,
                    all_metrics_opt, all_opt):
        """ Display information about an ocurrence (event or metric)

        Parameters:
            occurrence - the event or metric to be displayed.
            all_opt - if should display all ocurrences
            all_events_opt - if should display all events only
            all_metrics_opt - if should display all metrics only
        """
        processor = core.get_processor()
        core.supported_feature(processor, "Info")

        inf_h = InfoHandler()
        inf_h.show_info(occurrence, all_events_opt, all_metrics_opt, all_opt)
        return 0
