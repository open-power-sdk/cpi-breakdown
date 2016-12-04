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

import subprocess
import commands
import time


def execute(command):
    """Execute a command with its parameters"""
    try:
        return subprocess.check_call([command],
                                     stderr=subprocess.STDOUT,
                                     shell=True)
    except subprocess.CalledProcessError as e:
        return e.returncode


def cmdexists(command):
    """Check if a command exists"""
    subp = subprocess.call("type " + command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0


def get_processor():
    """Check the system processor"""
    return commands.getoutput("grep -io 'power[[:digit:]]\+' -m 1 /proc/cpuinfo")


def parse_file(output_stream, timestamp):
    """Read lines from output_stream file and writes it into another file in
    a dictionary format"""
    parsed_file = output_stream + "_" + timestamp
    with open(output_stream, "r") as f:
        for line in f:
            if not line.isspace():
                with open(parsed_file, "a+") as ff:
                    ff.write(line.split(",")[0] + " : ")
                    ff.write(line.split(",")[1] + "\n")


def get_timestamp():
    """Return the current timestamp"""
    return time.strftime("%Y%m%d_%H%M%S")


def file_to_dict(filename):
    """Read contents of a file and return it as a dictionary"""
    with open(filename, "r") as f:
        dictionary = {}
        for line in f:
            k, v = line.strip().split(" : ")
            dictionary[k] = v

    return dictionary
