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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import sys

from cpi import core

OPERF = "operf"
OPREPORT = "opreport"


def sort_events(events_dict):
    """ Receive a dictionary of events and their values and return a list
    with the events and values sorted. If it can not sort the events list
    force to exit """
    events = events_dict.items()
    try:
        events = sorted(events, key=lambda x: int(x[1]), reverse=True)
    except ValueError:
        sys.stderr.write("Could not perform the auto drilldown because "
                         "the specified file is not correctly formatted.\n"
                         "Select a properly formmatted file and run the "
                         "auto drilldown again\n")
        sys.exit(1)
    return events


def run_operf(binary_path, binary_args, event, min_count):
    """ Run operf and exit if an error happens """
    operf_cmd = OPERF + " -e {0}:{1} {2} {3}".format(event, min_count,
                                                     binary_path, binary_args)
    status, output = core.execute_stdout(operf_cmd)
    if status != 0:
        sys.stderr.write("Failed to run {0} command.\n".format(OPERF) +
                         "\n" + output)
        sys.exit(1)


def run_opreport(event, report_file):
    """ Run opreport and exit if an error happens """
    opreport_cmd = OPREPORT + " --debug-info --symbols --details "
    opreport_cmd += "--xml event:{0} -o {1}".format(event, report_file)

    status, output = core.execute_stdout(opreport_cmd)
    if status != 0:
        sys.stderr.write("Failed to run {0} command.\n".format(OPREPORT) +
                         "\n" + output)
        sys.exit(1)
