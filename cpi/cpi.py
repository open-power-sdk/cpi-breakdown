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
import argparse
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import pkg_resources

from controller import *


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
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message)
        subparsers = parser.add_subparsers(help="list of common CPI commands\n\n")

        # Execution
        parser_execution = subparsers.add_parser(
            'execute',
            formatter_class=RawTextHelpFormatter,
            help="collect the value of the events used in the breakdown\n"
                 "e.g: cpi execute -b <binary> '<binary_args>'\n"
                 "see cpi execute --help\n\n")
        parser_execution.add_argument(
            '-o', '--output',
            dest='output_path',
            type=str,
            default='',
            nargs=1,
            help="specify the directory to save the output of the execution")
        parser_execution.add_argument(
            '-b', '--binary',
            dest='binary_path',
            type=str, default='',
            required=True,
            help="specify the path to the application binary and its\n"
                 "arguments which are between single quotes")

        # Drilldown
        parser_drilldown = subparsers.add_parser(
            'drilldown',
            formatter_class=argparse.RawTextHelpFormatter,
            help="perform a drilldown execution for a specific event\n"
                 "e.g: cpi drilldown -e <event> -b <binary> '<binary_args>'\n"
                 "see cpi drilldown --help\n\n")
        parser_drilldown.add_argument(
            '-e', '--event',
            dest='event_name',
            type=str,
            default='',
            nargs=1,
            required=True,
            help="specify the event that will be used for drilldown")
        parser_drilldown.add_argument(
            '-b', '--binary',
            dest='binary_path',
            type=str,
            default='',
            required=True,
            help="specify the path to the application binary and its\n"
                 "arguments which are between single quotes")

        # Compare
        parser_compare = subparsers.add_parser(
            'compare',
            formatter_class=argparse.RawTextHelpFormatter,
            help="compare the collected results of two CPI executions and\n"
                 "provide feedback on performance variations\n"
                 "e.g: cpi compare -f file_1 file_2\n"
                 "see cpi compare --help")
        parser_compare.add_argument(
            '-f', '--files',
            dest="cpi_files",
            default='',
            type=str,
            nargs=2,
            required=True,
            metavar=('file_1', 'file_2'),
            help="specify the files to execute the comparation")
        parser_compare.add_argument('--sort',
                                    dest="sort_opt",
                                    action='store_true',
                                    help="sort values by percentage")

        # Process arguments
        args, application_args = parser.parse_known_args()
        ctrller = Controller()
        ctrller.run(args, application_args)
    except KeyboardInterrupt:
        return 1

if __name__ == "__main__":
    sys.exit(main())
