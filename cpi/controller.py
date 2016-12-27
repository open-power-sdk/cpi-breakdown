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
import errno

import core
import events_reader
from breakdown.breakdown_tree import BreakdownTree
from breakdown.breakdown_table import *
from drilldown.drilldown_view import DrilldownView
from info import info_handler
from metrics_calculator import MetricsCalculator
from compare import table_creator
from compare.comparator import Comparator


class Controller(object):
    """
    Controls the execution of CPI commands
    """
    def __init__(self):
        self.__binary_path = ''
        self.__binary_args = ''

    def run(self, args, application_args):
        """
        Executes the correct action according the user input
        """
        try:
            self.__binary_path = args.binary_path
        except AttributeError:
            self.__binary_path = ''
        if application_args:
            self.__binary_args = application_args[0]

        # Run compare
        if 'cpi_files' in args:
            self.__run_compare(args.cpi_files, args.sort_opt)
        # Run drilldown
        elif 'event_name' in args:
            self.__run_drilldown(args.event_name[0])
        # Run info
        elif 'event_info' in args:
            self.__show_info(args.event_info[0])
        # Run breakdown
        else:
            self.__run_cpi(args.output_path, args.table_format,
                           args.show_events)

    def __run_cpi(self, output_location, table_format, show_events):
        """ Run the breakdown feature """
        processor = core.get_processor()
        ocount = "ocount"
        core.supported_feature(processor, "Breakdown")
        if not os.path.isfile(self.__binary_path):
            sys.stderr.write(self.__binary_path + ' binary file not found\n')
            sys.exit(1)

        if not output_location:
            output_location = os.getcwd()
        else:
            try:
                if not os.path.isdir(output_location):
                    os.makedirs(output_location)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise sys.exit(1)

        timestamp = core.get_timestamp()
        binary_name = self.__binary_path.split("/").pop(-1)
        ocount_out = output_location + "/output"

        if not core.cmdexists(ocount):
            sys.stderr.write(ocount + " is not installed in the system. " +
                             "Install oprofile before continue." + "\n")
            sys.exit(2)

        reader = events_reader.EventsReader(processor)
        results_file_name = output_location + "/" + binary_name + "_" + timestamp + ".cpi"
        start_time = time.time()
        exec_counter = 0
        sys.stdout.write("\n")

        # Run ocount for all events groups
        for event in reader.get_events():
            exec_counter = exec_counter + 1
            ocount_cmd = ocount + " -b -f " + ocount_out
            for item in event:
                ocount_cmd += " -e " + item
            sys.stdout.write("\r    Executing CPI Breakdown: %d/%d iterations \
                             (elapsed time: %d seconds)"
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
            core.parse_file(ocount_out, results_file_name)
        sys.stdout.write("\n\n")
        core.execute("rm " + ocount_out)

        try:
            events = core.file_to_dict(results_file_name)
        except ValueError:
            sys.stderr.write("File {} was not correctly formatted.\n"
                             "{} may have failed when generating the report "
                             "file. Try to run breakdown feature again\n"
                             .format(results_file_name, ocount))
            sys.exit(1)

        # Calculate metrics values
        metrics_calc = MetricsCalculator(processor)
        metrics_value = metrics_calc.calculate_metrics(events)

        # Show breakdown output
        if table_format:
            table = MetricsTable(metrics_value)
            table.print_table()
        else:
            tree = BreakdownTree(metrics_calc.get_raw_metrics(), metrics_value)
            tree.print_tree()

        # Show events values
        if show_events:
            events_table = EventsTable(events)
            events_table.print_table()

    def __run_drilldown(self, event):
        """ Run the drilldown feature """
        operf = "operf"
        opreport = "opreport"
        processor = core.get_processor()
        core.supported_feature(processor, "Drilldown")

        if not os.path.isfile(self.__binary_path):
            sys.stderr.write(self.__binary_path + ' binary file not found\n')
            sys.exit(1)

        if not core.cmdexists(operf):
            sys.stderr.write(operf + " is not installed in the system. " +
                             "Install oprofile before continue." + "\n")
            sys.exit(2)

        reader = events_reader.EventsReader(processor)

        # Event is not supported with drilldown feature
        if not reader.valid_event(event):
            sys.stderr.write("Event {0} is not supported by drilldown \
                             feature.".format(event) +
                             "\nChoose a supported event and try again\n")
            sys.exit(1)

        # Run operf command
        min_count = str(reader.get_event_mincount(event))
        operf_cmd = operf + " -e {0}:{1} {2} {3}".format(event, min_count,
                                                         self.__binary_path,
                                                         self.__binary_args)
        status = core.execute(operf_cmd)
        if status != 0:
            sys.stderr.write("Failed to run {0} command.\n".format(operf) +
                             "For more information check the error message \
                             above\n")
            sys.exit(1)

        # Run opreport command
        report_file = "opreport.xml"
        opreport_cmd = opreport + " --debug-info --symbols --details "
        opreport_cmd += "--xml event:{0} -o {1}".format(event, report_file)
        status = core.execute(opreport_cmd)
        if status != 0:
            sys.stderr.write("Failed to run {0} command.\n".format(opreport) +
                             "For more information check the error message \
                             above\n")
            sys.exit(1)

        drilldown_view = DrilldownView()
        drilldown_view.print_drilldown(event, report_file)

    def __run_compare(self, file_names, sort_opt):
        """ Get the contents of two ocount output files, compare their results
        and display in a table """
        dict_list = []
        final_array = []

        # Create a list with two dictionaries containing "event:value" pairs
        for file_name in file_names:
            if not os.path.isfile(file_name):
                print file_name + ' file not found\n'
                return final_array
            try:
                dict_i = core.file_to_dict(file_name)
                dict_list.append(dict_i)
            except ValueError:
                sys.stderr.write("Could not parse {} file.\n"
                                 "Select a properly formatted file and run "
                                 "the compare feature again\n".format(
                                     file_name))
                sys.exit(1)

        try:
            comparator = Comparator(dict_list)
            final_array = comparator.compare()
        except (KeyError, ValueError):
            sys.stderr.write("Could not perform the comparison between files."
                             "\nSelect properly formatted files and run the "
                             "compare feature again.\n")
            sys.exit(1)

        table_creator.create_table(file_names, final_array, sort_opt)

    def __show_info(self, event_info):
        """ Display information about an event (event_info) """
        ih = info_handler.InfoHandler(event_info)
        ih.show_events_info(event_info)
        return 0
