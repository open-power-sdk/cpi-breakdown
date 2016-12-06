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

import commands
import core
import os
import sys

import events_reader
import metrics_calculator


def run_cpi(binary_path, binary_args, output_location):
    '''
    Uses the current path as destination if nothing is set
    by the user.
    '''
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
    ocount_out = output_location + "/ocount_out"

    if not core.cmdexists("ocount"):
        sys.stderr.write("ocount is not installed in the system. " +
                         "Install oprofile before continue." + "\n")
        sys.exit(0)

    reader = events_reader.EventsReader(core.get_processor())
    for event in reader.get_events():
        ocount = "ocount -b -f " + ocount_out
        for item in event:
            ocount += " -e " + item
        print "\n" + "Running: " + ocount + " " + binary_path + binary_args
        core.execute(ocount + ' ' + binary_path + binary_args)
        core.parse_file(ocount_out, timestamp)
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


def run_drilldown(event, binary_path, binary_args):
    """ Run the drilldown feature """
    if not core.cmdexists("operf"):
        sys.stderr.write("operf is not installed in the system. " +
                         "Install oprofile before continue." + "\n")
        sys.exit(0)

    reader = events_reader.EventsReader(core.get_processor())

    # Event is not supported with drilldown feature
    if not reader.valid_event(event):
        sys.stderr.write("Event {0} is not supported by drilldown feature.".format(event) +
                         "\nChoose a supported event and try again\n")
        sys.exit(0)

    # Run operf command
    event_min_count = str(reader.get_event_mincount(event))
    operf_cmd = "operf -e {0}:{1} {2} {3}".format(event, event_min_count, binary_path, binary_args)
    core.execute(operf_cmd)

    # Run opreport command
    temp_file = "opreport.xml"
    opreport_cmd = "opreport --debug-info --symbols --details --xml event:{0} -o {1}".format(
        event, temp_file)
    core.execute(opreport_cmd)

    # TODO: Implement the parser for the generated file
