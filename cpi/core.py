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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
"""
import os
import subprocess
import commands
import time
import re
import csv
import sys

# List with supported processors for hardware dependent cpi features
SUPPORTED_PROCESSORS = ["POWER8"]


def execute(command):
    """ Execute a command with its parameters and return the exit code """
    try:
        return subprocess.check_call([command], stderr=subprocess.STDOUT,
                                     shell=True)
    except subprocess.CalledProcessError as e:
        return e.returncode


def execute_stdout(command):
    """ Execute a command with its parameter and return the exit code
    and the command output """
    try:
        subprocess.check_output([command], stderr=subprocess.STDOUT,
                                shell=True)
        return 0, ""
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output


def cmdexists(command):
    """Check if a command exists"""
    subp = subprocess.call("type " + command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0


def get_processor():
    """Check the system processor"""
    return commands.getoutput("grep -io 'power[[:digit:]]\+' -m 1 /proc/cpuinfo")


def supported_processor(processor_version):
    """Check if processor is supported"""
    return processor_version in SUPPORTED_PROCESSORS


def supported_feature(processor, feature_name):
    """Check whether a feature is supported. If it is not supported,
    force the execution to finish"""
    if not supported_processor(processor):
        sys.stderr.write("{} feature is not supported on {}\n"
                         .format(feature_name, processor))
        sys.exit(1)


def parse_file(output_stream, event_values):
    """Parse the ocount output file to get events and values"""
    with open(output_stream, "r") as infile:
        for line in infile:
            if not line.isspace():
                key_val = line.split(",")[0].strip()
                val = line.split(",")[1].strip()
                event_values[key_val] = val
    return event_values


def save_events(events, file_name):
    """Save events values into file"""
    with open(file_name, "w") as ev_file:
        for key in events:
            ev_file.write(key + " : " + events[key] + "\n")


def get_timestamp():
    """Return the current timestamp"""
    return time.strftime("%Y%m%d_%H%M%S")


def file_to_dict(filename):
    """Read contents of a file and return it as a dictionary.
    The file should be in format: event_name : envent_value
    """
    dictionary = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                k, v = line.strip().split(" : ")
                dictionary[k] = v
    except ValueError:
        raise ValueError
    except IOError:
        raise IOError
    return dictionary


def percentage(init_val, final_val):
    """Calculate a percentage relative to the initial amount of two values"""
    value = 100 * (final_val - init_val) / float(init_val)
    return "%.2f" % value
