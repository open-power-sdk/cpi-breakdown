#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C) 2017 IBM Corporation

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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
'''

import sys
import argparse
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import pkg_resources

from cpi.controller import Controller

__all__ = []
__version__ = pkg_resources.require("cpi")[0].version


class CLIError(Exception):
    '''Error treatment'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    '''CPI main function'''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version = "v%s" % __version__
    program_version_message = '%%(prog)s %s ' % (program_version)
    program_shortdesc = '''
    --- Cycles Per Instruction (CPI) ---
    Profiles C/C++ applications with the CPI (cycles per instruction)
    breakdown model for POWER8 and POWER9.'''

    try:
        parser = ArgumentParser(description=program_shortdesc,
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message)
        subparsers = parser.add_subparsers(help='\nCPI commands\n\n')

        # Data Record
        parser_record = subparsers.add_parser(
            'record',
            formatter_class=RawTextHelpFormatter,
            help='collect and record the events used in the breakdown\n'
                 'see cpi record --help\n\n')
        parser_record.add_argument(
            '-q', '--quiet',
            dest='quiet',
            action='store_true',
            help='suppress the progress indicator during the\n'
                 'recording step\n'
                 'e.g: cpi record -q <command>')
        parser_record.add_argument(
            '-o', '--output',
            dest='output_file',
            type=str,
            default='',
            help='specify the name of the output file which is created\n'
                 'during the recording step\n'
                 'e.g: cpi record -o <output_file> <command>')
        parser_record.add_argument(
            dest='cmd',
            type=str,
            default=None,
            metavar='COMMAND',
            nargs=1,
            help='the application and its arguments\n'
                 'e.g: cpi record <command>\n'
                 '     cpi record /usr/bin/ls -la')
        parser_record.add_argument(
            dest='cmd_args',
            type=str,
            default=None,
            nargs=argparse.REMAINDER,
            help=argparse.SUPPRESS)

        # Data Display
        parser_display = subparsers.add_parser(
            'display',
            formatter_class=RawTextHelpFormatter,
            help='display the result of the data collected during the \n'
                 'recording step\n'
                 'see cpi display --help\n\n')
        parser_display.add_argument(
            '--format',
            dest='breakdown_format',
            type=str,
            choices=['tree', 'table'], default='tree',
            help='specify the format of the breakdown output (default is tree)\n'
                 'e.g: cpi display --format=table -f <file.cpi>')
        parser_display.add_argument(
            '--top-events',
            dest='top_events',
            metavar='N',
            type=int,
            help='show the N highest events. This option suppresses \n'
                 'the breakdown output\n'
                 'e.g: cpi display --top-events=3 -f <file.cpi>')
        parser_display.add_argument(
            '--top-metrics',
            dest='top_metrics',
            metavar='N',
            type=int,
            help='show the N highest metrics. This option suppresses \n'
                 'the breakdown output\n'
                 'e.g: cpi display --top-metrics=3 -f <file.cpi>')
        parser_display.add_argument(
            '-f', '--file',
            dest='display_file',
            metavar='CPI_FILE',
            required=True,
            type=str,
            help='the .cpi files that contains the events values\n'
                 'e.g: cpi display -f <file.cpi>')

        # Drilldown
        parser_drilldown = subparsers.add_parser(
            'drilldown',
            epilog='One of the arguments -e/--event or -a/--auto is required '
                   'to run drilldown.',
            formatter_class=argparse.RawTextHelpFormatter,
            help='perform a drilldown execution for a specific event\n'
                 'see cpi drilldown --help\n\n')
        drilldown_group = parser_drilldown.add_mutually_exclusive_group(
            required=True)
        drilldown_group.add_argument(
            '-e', '--event',
            dest='event_name',
            type=str,
            help='specify the event that will be used for drilldown\n'
                 'e.g: cpi drilldown -e <EVENT_NAME> <command>')
        drilldown_group.add_argument(
            '-a', '--auto',
            dest='autodrilldown',
            metavar='N',
            type=int,
            help='perform drilldown on the N highest events\n'
                 'e.g: cpi drilldown -a 5 <command>')
        parser_drilldown.add_argument(
            '-f', '--file',
            dest='autodrilldown_file',
            metavar='CPI_FILE',
            type=str,
            help='allow auto-drilldown to consume events from a previously\n'
                 'generated .cpi file\n'
                 'e.g: cpi drilldown -a 5 -f <file.cpi> <command>')
        parser_drilldown.add_argument(
            '-t', '--threshold',
            dest='threshold',
            metavar='N',
            type=float,
            help='do not display drilldown for symbols less than N%%\n'
                 'e.g: cpi drilldown -t 5.5 -e <EVENT_NAME> <command>\n'
                 '     cpi drilldown -t 6 -a 4 -f <file.cpi> <command>')
        parser_drilldown.add_argument(
            dest='cmd',
            type=str,
            default=None,
            metavar='COMMAND',
            nargs=1,
            help='the application and its arguments\n'
                 'e.g: cpi drilldown <command>\n'
                 '     cpi drilldown /usr/bin/ls -la')
        parser_drilldown.add_argument(
            dest='cmd_args',
            type=str,
            default=None,
            nargs=argparse.REMAINDER,
            help=argparse.SUPPRESS)

        # Compare
        parser_compare = subparsers.add_parser(
            'compare',
            formatter_class=argparse.RawTextHelpFormatter,
            help='compare the collected results of two CPI executions and\n'
                 'provide feedback on performance variations\n'
                 'see cpi compare --help\n\n')
        parser_compare.add_argument(
            '-f', '--files',
            dest='cpi_files',
            default='',
            type=str,
            nargs=2,
            required=True,
            metavar=('file_1.cpi', 'file_2.cpi'),
            help='specify the files on which to execute the comparison\n'
                 'e.g: cpi compare -f <file_1.cpi> <file_2.cpi>')
        parser_compare.add_argument(
            '-t', '--type',
            dest='type_opt',
            type=str,
            choices=['event', 'metric'], default='event',
            help='choose between metric or event to compare (default is event)\n'
                 'e.g: cpi compare -t=metric -f <file_1.cpi> <file_2.cpi>')
        parser_compare.add_argument(
            '-c', '--csv',
            dest='csv',
            action='store_true',
            help='show the compare output in a csv format\n'
                 'e.g: cpi compare -c -f <file_1.cpi> <file_2.cpi>')

        # Show_info
        parser_info = subparsers.add_parser(
            'info',
            formatter_class=argparse.RawTextHelpFormatter,
            help='show information about events and metrics\n'
                 'see cpi info --help')
        info_group = parser_info.add_mutually_exclusive_group(
            required=True)
        info_group.add_argument(
            '-c', '--component',
            dest='occurrence_info',
            type=str,
            metavar='EVENT/METRIC',
            default='',
            nargs=1,
            help='display information about CPI components which\n'
                 'can be either metrics or events\n'
                 'e.g: cpi info -c <EVENT_NAME>\n'
                 '     cpi info -c <METRIC_NAME>')
        info_group.add_argument(
            '-a', '--all',
            dest='all_opt',
            action='store_true',
            help='show information for all events and metrics\n'
                 'e.g: cpi info --all')
        info_group.add_argument(
            '--all-events',
            dest='all_events_opt',
            action='store_true',
            help='show all events supported by cpi\n'
                 'e.g: cpi info --all-events')
        info_group.add_argument(
            '--all-metrics',
            dest='all_metrics_opt',
            action='store_true',
            help='show all metrics supported by cpi\n'
                 'e.g: cpi info --all-metrics')

        # Process arguments
        args = parser.parse_args()
        if len(vars(args).keys()) == 0:
            parser.print_usage()
            return 1

        ctrller = Controller()
        ctrller.run(args)

    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
