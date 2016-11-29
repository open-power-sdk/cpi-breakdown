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
import sys
import commands


def execute(command, output_stream=None):
    """execute a command with its parameters"""
    if output_stream is not None:
        try:
            return subprocess.check_call([command],
                                         stdout=open(output_stream, "a+"),
                                         shell=True)
        except subprocess.CalledProcessError as e:
            return e.returncode
    elif output_stream is None:
        try:
            return subprocess.check_call([command],
                                         stderr=subprocess.STDOUT,
                                         shell=True)
        except subprocess.CalledProcessError as e:
            return e.returncode


def cmdexists(command):
    """check if a command exists"""
    subp = subprocess.call("type " + command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0


def get_processor():
    """Check the system processor"""
    return commands.getoutput("grep -io 'power[[:digit:]]\+' -m 1 /proc/cpuinfo")
