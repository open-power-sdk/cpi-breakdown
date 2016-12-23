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
import os.path
import sys
import time
import errno
from terminaltables import AsciiTable

import core
import events_reader
from breakdown_tree import BreakdownTree
from drilldown.drilldown_view import DrilldownView
from metrics_calculator import MetricsCalculator
from compare import table_creator
from compare.comparator import Comparator


class Controller(object):
    """
    Controls the execution of CPI commands
    """
    __application_args = ''

    def run(self, args, application_args):
        '''
        Executes the correct action according the user input
        '''
        if application_args:
            self.__application_args = application_args[0]

        if 'cpi_files' in args:
            self.__run_compare(args.cpi_files)
        elif 'event_name' in args:
            self.__run_drilldown(args.event_name[0],
                                 args.binary_path,
                                 self.__application_args)
        else:
            self.__run_cpi(args.binary_path,
                           self.__application_args,
                           args.output_path)

    @classmethod
    def __run_cpi(cls, binary_path, binary_args, output_location):
        """ Run the breakdown feature """
        processor = core.get_processor()
        ocount = "ocount"
        core.supported_feature(processor, "Breakdown")
        if not os.path.isfile(binary_path) or not os.access(binary_path, os.X_OK):
            sys.stderr.write('Something wrong with ' + binary_path +
                             ' file. Check if it is a valid binary path\n')
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
        binary_name = binary_path.split("/").pop(-1)
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
                                                 binary_path + ' ' +
                                                 binary_args)
            if status != 0:
                sys.stderr.write("\n\nFailed to run {0} command.".
                                 format(ocount) + "\n" + output + "\n")
                sys.exit(1)
            core.parse_file(ocount_out, results_file_name)
        sys.stdout.write("\n\n")
        core.execute("rm " + ocount_out)

        metrics_calc = MetricsCalculator(processor)
        try:
            events = core.file_to_dict(results_file_name)
        except ValueError:
            sys.stderr.write("File {} was not correctly formatted.\n"
                         "{} may have failed when generating the report file. "
                         "Try to run breakdown feature again\n"
                         .format(results_file_name, ocount))
            sys.exit(1)

        metrics_value = metrics_calc.calculate_metrics(events)

        tree = BreakdownTree(metrics_calc.get_raw_metrics(), metrics_value)
        tree.print_tree()

        met_table = [['Metric', 'Value', 'Percentage']]
        for row in metrics_value:
            met_table.append(row)
        met_tab = AsciiTable(met_table)
        print met_tab.table

        return

    @classmethod
    def __run_drilldown(cls, event, binary_path, binary_args):
        """ Run the drilldown feature """
        operf = "operf"
        opreport = "opreport"
        processor = core.get_processor()
        core.supported_feature(processor, "Drilldown")

        if not os.path.isfile(binary_path):
            sys.stderr.write(binary_path + ' binary file not found\n')
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
        event_min_count = str(reader.get_event_mincount(event))
        operf_cmd = operf + " -e {0}:{1} {2} {3}".format(event, event_min_count, binary_path, binary_args)
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

    @classmethod
    def __run_compare(cls, file_names):
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
            sys.stderr.write("Could not perform the comparison between files.\n"
                             "Select properly formatted files and run the "
                             "compare feature again.\n")
            sys.exit(1)

        table_creator.create_table(file_names, final_array)
