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

import core
import os
import sys

import events_reader
from drilldown.drilldown_view import DrilldownView


def run_cpi(binary_path, binary_args, output_location, advance_toolchain):
    '''
    Uses the current path as destination if nothing is set
    by the user.
    '''
    tool_prefix = ''
    if advance_toolchain:
        tool_prefix = "/opt/" + advance_toolchain + "/bin/"

    if not output_location:
        output_location = os.getcwd()
    else:
        try:
            if not (os.path.isdir(output_location)):
                os.makedirs(output_location)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
                sys.exit(0)

    timestamp = core.get_timestamp()
    ocount_out = output_location + "/output"

    if not core.cmdexists(tool_prefix + "ocount"):
        sys.stderr.write(tool_prefix + "ocount is not installed in the system. " +
                         "Install oprofile before continue." + "\n")
        sys.exit(0)

    reader = events_reader.EventsReader(core.get_processor())
    for event in reader.get_events():
        ocount = tool_prefix + "ocount -b -f " + ocount_out
        for item in event:
            ocount += " -e " + item
        print "\n" + "Running: " + ocount + " " + binary_path + binary_args
        core.execute(ocount + ' ' + binary_path + binary_args)
        core.parse_file(ocount_out, timestamp, ".cpi")
    core.execute("rm " + ocount_out)
    '''
    TODO: calculate metrics here
    mc = MetricsCalculator(core.get_processor())
    events_result = defaultdict(list)
    with open("./output") as fin:
        for line in fin:
            k, v = line.strip().split(" : ")
            events_result[k].append(v)
    print mc.calculate_metrics(events_result)
    '''
    return


def compare_output(file_names):
    """ Get the contents of two ocount output files and compare their
        results. Return a list with all values and percentage """
    dict_list = []
    final_array = []

    # Create a list with two dictionaries containing "event:value" pairs
    for file_name in file_names:
        dict_i = core.file_to_dict(file_name)
        dict_list.append(dict_i)

    # Create one dictionary as {"events" : (val_file_1, val_file_2), ...}
    dict_vals = {}
    for key in dict_list[0]:
        dict_vals[key] = tuple(d[key] for d in dict_list)

    # Create final_array, with event names, values and percentages
    for key in dict_vals:
        try:
            if int(dict_vals[key][0]) != 0:
                percentage = core.percentage(int(dict_vals[key][1]),
                                             int(dict_vals[key][0]))
            else:
                percentage = "-"
            final_array.append([key, dict_vals[key][0], dict_vals[key][1],
                         percentage])
        except IndexError:
            sys.exit(1)

    return final_array


def run_drilldown(event, binary_path, binary_args, advance_toolchain):
    """ Run the drilldown feature """
    operf = "operf"
    opreport = "opreport"
    if advance_toolchain:
        operf = "/opt/" + advance_toolchain + "/bin/" + operf
        opreport = "/opt/" + advance_toolchain + "/bin/" + opreport

    if not core.cmdexists(operf):
        sys.stderr.write(operf + " is not installed in the system. " +
                         "Install oprofile before continue." + "\n")
        sys.exit(2)

    reader = events_reader.EventsReader(core.get_processor())

    # Event is not supported with drilldown feature
    if not reader.valid_event(event):
        sys.stderr.write("Event {0} is not supported by drilldown feature.".format(event) +
                         "\nChoose a supported event and try again\n")
        sys.exit(1)

    # Run operf command
    event_min_count = str(reader.get_event_mincount(event))
    operf_cmd = operf + " -e {0}:{1} {2} {3}".format(event, event_min_count,
                                                     binary_path, binary_args)
    status = core.execute(operf_cmd)
    if status != 0:
        sys.stderr.write("Failed to run {0} command.\n".format(operf) +
                         "For more information check the error message above")
        sys.exit(1)

    # Run opreport command
    report_file = "opreport.xml"
    opreport_cmd = opreport + " --debug-info --symbols --details "
    opreport_cmd += "--xml event:{0} -o {1}".format(event, report_file)
    status = core.execute(opreport_cmd)
    if status != 0:
        sys.stderr.write("Failed to run {0} command.\n".format(opreport) +
                         "For more information check the error message above")
        sys.exit(1)

    drilldown_view = DrilldownView()
    drilldown_view.print_drilldown(event, report_file)
