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
import pkg_resources
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import controller
import core
import table_creator

__all__ = []
__version__ = pkg_resources.require("cpi")[0].version


class CLIError(Exception):
    """Error treatment"""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    """CPI main function"""
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

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
                            To learn about Advance Toolchain access ibm.co/AdvanceToolchain.")
        parser.add_argument('--drilldown', dest="drilldown_args", type=str, default='',
                            metavar="event_name",
                            help="Use the drilldown feature with the given event", nargs="+")
        parser.add_argument('-c', '--compare', dest="file_names", default='',
                            metavar=('output_1', 'output_2'), type=str,
                            help="Compare different runs passing a list of\
                            files.", nargs=2)
        parser.add_argument(dest="application_path", type=str,
                            help="path to the application binary and its arguments",
                            default='', nargs='*')

        # Process arguments
        args, application_args = parser.parse_known_args()

        if not args.application_path and not args.file_names and not args.drilldown_args:
            parser.print_usage()
            exit(1)

        drilldown_args = args.drilldown_args
        file_names = args.file_names

        # Run compare runs
        if file_names:
            table_creator.table_creator(file_names)
            exit(0)

        # Run CPI (counter)
        if args.application_path and not drilldown_args:
            print 'run cpi'
            [binary_path, binary_args] = get_binary_path_args(args.application_path,
                                                              application_args)
            controller.run_cpi(binary_path, binary_args,
                               args.output_location,
                               args.advance_toolchain)
            exit(0)

        # Run drilldown (profiler)
        if drilldown_args:
            binary_path = ''
            event_name = ''
            binary_args = ' '

            if len(drilldown_args) == 1 and not args.application_path:
                event_name = drilldown_args[0]
                sys.stderr.write("For drilldown, you must set an event and a binary path\n")
                return 1

            if len(drilldown_args) >= 2:
                [binary_path, binary_args] = get_binary_path_args(drilldown_args[1:],
                                                                  application_args)
                event_name = drilldown_args[0]

            if len(args.application_path) > 0:
                [binary_path, binary_args] = get_binary_path_args(args.application_path,
                                                                  application_args)
                event_name = drilldown_args[0]

            controller.run_drilldown(event_name, binary_path, binary_args, args.advance_toolchain)

    except KeyboardInterrupt:
        return 1

def get_binary_path_args(app_path, application_args):
    """ Return binary path and binary args """
    binary_path = app_path.pop(0)
    # If a binary argument contains space, it was passed inside quotes
    binary_args = ' ' + ' '.join((i if " " not in i else "'" + i + "'")
                                 for i in app_path)
    binary_args += ' ' + ' '.join((i if " " not in i else "'" + i + "'")
                                  for i in application_args)

    return binary_path, binary_args


if __name__ == "__main__":
    sys.exit(main())
