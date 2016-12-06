#! /usr/bin/env python
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

import sys
import os
import time
import pkg_resources
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import controller
import core

__all__ = []
__version__ = pkg_resources.require("cpi")[0].version


class CLIError(Exception):
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_version_message = '%%(prog)s %s ' % (program_version)
    program_shortdesc = '''
    --- Cycles Per Instruction (CPI) ---
    Profiles C/C++ applications with the CPI (cycles per instruction) breakdown
    model for POWER8.'''

    try:
        parser = ArgumentParser(description=program_shortdesc,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)
        parser.add_argument("-o", "--output-location", dest="output_location",
                            type=str,
                            help="the location where to store the result of the execution.\
                            e.g.: --output-location=<path>",
                            nargs='?')
        parser.add_argument('--advance-toolchain', dest='advance_toolchain',\
                            choices=core.get_installed_at(),\
                            help="allows selecting oprofile from an \
                            installed version of Advance Toolchain instead of\
                            using the installed version of the system.\
                            e.g.: --advance-toolchain=at10.0.\
                            To learn about Advance Toolchain access ibm.co/AdvanceToolchain."
                            )
        parser.add_argument('--drilldown', dest="event_name", type=str,
                            help="Use the drilldown feature with the given event", nargs="?")
        parser.add_argument(dest="application_path",
                            help="path to the application binary and its arguments",
                            nargs='+')

        # Process arguments
        args, application_args = parser.parse_known_args()
        event_name = args.event_name
        binary_path = args.application_path.pop(0)
        binary_args = ' ' + ' '.join(map(str, args.application_path))
        binary_args += ' ' + ' '.join(map(str, application_args))

        # Run CPI (counter)
        if event_name is None:
            controller.run_cpi(binary_path, binary_args, args.output_location, args.advance_toolchain)
        # Run drilldown (profiler)
        else:
            controller.run_drilldown(event_name, binary_path, binary_args, args.advance_toolchain)

    except KeyboardInterrupt:
        return 0
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help" + "\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
