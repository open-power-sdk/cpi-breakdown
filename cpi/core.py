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
        sys.stderr.write("{} feature is not supported in processor: {}\n"
                         .format(feature_name, processor))
        sys.exit(1)


def parse_file(output_stream_file, parsed_file):
    """Read lines from output_stream_file and writes it into another file as
    a dictionary. The output_stream_file should be in format:
        event_name,event_value,percentage
    """
    with open(output_stream_file, "r") as f:
        for line in f:
            if not line.isspace():
                with open(parsed_file, "a+") as ff:
                    ff.write(line.split(",")[0] + " : ")
                    ff.write(line.split(",")[1] + "\n")


def get_timestamp():
    """Return the current timestamp"""
    return time.strftime("%Y%m%d_%H%M%S")


def file_to_dict(filename):
    """Read contents of a file and return it as a dictionary.
    The file should be in format: event_name : envent_value
    """
    dictionary = {}
    with open(filename, "r") as f:
        try:
            for line in f:
                k, v = line.strip().split(" : ")
                dictionary[k] = v
        except ValueError:
            raise ValueError
    return dictionary


def get_installed_at():
    """Gets the AT version installed in the system"""
    at_pattern = re.compile("^at([0-9]?[0-9]).[0-9]$")
    installed_at = []
    for directory in os.listdir("/opt"):
        if at_pattern.match(str(directory)):
            installed_at.append(directory)
    if len(installed_at) > 0:
        return installed_at
    else:
        installed_at.append(" Advance Toolchain is not installed ")
        return installed_at


def percentage(init_val, final_val):
    """Calculate a percentage relative to the initial amount of two values"""
    value = 100 * (final_val - init_val) / float(init_val)
    return "%.2f" % value
