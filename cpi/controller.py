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
"""

import commands
import core
import os
import sys

import events_reader


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

    ocount_out = output_location + "/ocount_out." + str(core.get_timestamp())

    if not core.cmdexists("ocount"):
        sys.stderr.write("ocount package is not installed in the system. " +
                         "Install oprofile before continue." + "\n")
        sys.exit(0)
    for event in events_reader.get_events(core.get_processor()):
        ocount = "ocount -b"
        for item in event:
            ocount += " -e " + item
        print "\n" + "Running: " + ocount + " " + binary_path + binary_args
        core.execute(ocount + ' ' + binary_path + binary_args,  ocount_out)
    core.parse_file(ocount_out)
    return
