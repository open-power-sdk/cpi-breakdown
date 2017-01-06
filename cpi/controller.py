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
import metrics_calculator
from info.info_handler import InfoHandler
from breakdown.breakdown_tree import BreakdownTree
from breakdown.breakdown_table import MetricsTable
from breakdown.breakdown_table import EventsTable
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

    def run(self, args, application_args):
        """
        Executes the correct action according the user input.

        Parameters:
            args - arguments collected by argparser
            application_args - the application binary arguments
        """
        try:
            self.__binary_path = args.binary_path
        except AttributeError:
            self.__binary_path = ''
        if application_args:
            self.__binary_args = application_args[0]

        # Run compare
        if 'cpi_files' in args:
            self.__run_compare(args.cpi_files, args.sort_opt, args.csv)
        # Run drilldown
        elif 'event_name' in args:
            self.__run_drilldown(args.event_name, args.autodrilldown,
                                 args.autodrilldown_file, args.threshold)
        # Run info
        elif 'occurrence_info' in args:
            self.__show_info(args.occurrence_info, args.all_events_opt,
                             args.all_metrics_opt, args.all_opt)
        # Run breakdown
        else:
            self.__run_cpi(args.output_path, True, args.table_format,
                           args.show_events, args.hot_spots, args.quiet)

    def __run_cpi(self, output_location, show_breakdown, table_format,
                  show_events, hot_spots, quiet):
        """ Run the breakdown feature and return a formatted events file
        with .cpi extension

        Parameters:
            output_location - the path where the cpi file will be generated
            show_breakdown - if should show the breakdown model
            table_format - if should show the breakdown in a table format
            show_events - if should show the events values
            hot_spots - if should show hot spots for top 'n' events and metrics
            quiet - if should suppress the bar and breakdown output during run
        """
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

        # Run ocount for all events groups
        for event in reader.get_events():
            exec_counter = exec_counter + 1
            ocount_cmd = ocount + " -b -f " + ocount_out
            for item in event:
                ocount_cmd += " -e " + item
            if not quiet:
                sys.stdout.write("\r    Executing CPI Breakdown: %d/%d "
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
            core.parse_file(ocount_out, results_file_name)
        core.execute("rm " + ocount_out)

        try:
            events = core.file_to_dict(results_file_name)
        except IOError:
            sys.stderr.write(results_file_name + " file not found\n")
            sys.exit(1)
        except ValueError:
            sys.stderr.write("File {} was not correctly formatted.\n"
                             "{} may have failed when generating the report "
                             "file. Try to run breakdown feature again\n"
                             .format(results_file_name, ocount))
            sys.exit(1)

        # Calculate metrics values
        metrics_calc = metrics_calculator.MetricsCalculator(processor)
        metrics_value = metrics_calc.calculate_metrics(events)

        # Show breakdown model
        show_breakdown = False if quiet else show_breakdown
        if show_breakdown:
            sys.stdout.write("\n\n")
            if table_format:
                table = MetricsTable(metrics_value)
                table.print_table()
            else:
                tree = BreakdownTree(metrics_calc.get_raw_metrics(),
                                     metrics_value)
                tree.print_tree()

        # Show events values
        if show_events:
            events_table = EventsTable(events)
            events_table.print_table()

        # Show events and metrics hot spots
        if hot_spots:
            hs = HotSpots(hot_spots, metrics_value, events)
            hs.print_hotspots()

        return results_file_name

    def __run_drilldown(self, event, autodrilldown, autodrilldown_file,
                        threshold):
        """ Run the drilldown feature

        Parameters:
            event - the event to be used in drilldown
            autodrilldown - run autodrilldown in top 'n' events
            autodrilldown_file - run the autodrilldown using values from a
                                generated file
            threshold - the threshold value to show groups
        """
        processor = core.get_processor()
        core.supported_feature(processor, "Drilldown")

        if not os.path.isfile(self.__binary_path):
            sys.stderr.write(self.__binary_path + ' binary file not found\n')
            sys.exit(1)

        operf = drilldown_core.OPERF
        if not core.cmdexists(operf):
            sys.stderr.write(operf + " is not installed in the system. " +
                             "Install oprofile before continue." + "\n")
            sys.exit(2)

        # Running autodrilldown generating a .cpi file
        if autodrilldown and not autodrilldown_file:
            events_file = self.__run_cpi(None, False, False, False, None, False)
        # Running autodrilldown using an already created file
        elif autodrilldown and autodrilldown_file:
            events_file = autodrilldown_file

        if autodrilldown:
            try:
                events = core.file_to_dict(events_file)
            except IOError:
                sys.stderr.write(events_file + " file not found")
                sys.exit(1)
            except ValueError:
                sys.stderr.write("Could not parse {} file.\n"
                                 "Select a properly formatted file and run "
                                 "the auto drilldown again\n".format(
                                     events_file))
                sys.exit(1)
        else:
            events = {event: '0'}

        events = drilldown_core.sort_events(events)
        if autodrilldown:
            # Use the 'n' first elements
            events = events[:autodrilldown]

        reader = events_reader.EventsReader(processor)
        # Run drilldown with chosen events
        for element in events:
            event = element[0]
            # Event is not supported with drilldown feature
            if not reader.valid_event(event):
                sys.stderr.write("Event {0} is not supported by drilldown \
                                 feature.".format(event) +
                                 "\nChoose a supported event and try again\n")
                sys.exit(1)

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

    def __run_compare(self, file_names, sort_opt, csv_file):
        """ Get the contents of two ocount output files, compare their results
        and display in a table

        Parameters:
            file_names - cpi formatted file names
            sort_opt - if should sort the compare
            csv_file - if should redirect the comparison result to a csv file
        """
        dict_list = []
        final_array = []

        # Create a list with two dictionaries containing "event:value" pairs
        for file_name in file_names:
            try:
                dict_i = core.file_to_dict(file_name)
                dict_list.append(dict_i)
            except IOError:
                sys.stderr.write(file_name + " file not found")
                sys.exit(1)
            except ValueError:
                sys.stderr.write("Could not parse {} file.\n"
                                 "Select a properly formatted file and run "
                                 "the compare feature again\n".format(
                                     file_name))
                sys.exit(1)

        try:
            comparator = Comparator(dict_list)
            final_array = comparator.compare(sort_opt)
        except (KeyError, ValueError):
            sys.stderr.write("Could not perform the comparison between files."
                             "\nSelect properly formatted files and run the "
                             "compare feature again.\n")
            sys.exit(1)

        compare_view = CompareView(final_array)
        if csv_file:
            compare_view.save_to_file("cpi_compare.csv")
        else:
            compare_view.create_table(file_names)

    def __show_info(self, occurrence, all_events_opt,
                    all_metrics_opt, all_opt):
        """ Display information about an ocurrence (event or metric) """
        ih = InfoHandler()
        ih.show_info(occurrence, all_events_opt, all_metrics_opt, all_opt)
        return 0
