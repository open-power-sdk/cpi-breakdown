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


from drilldown_model import DrilldownModel
from opreport_model import *

TABULATION = "    "


class DrilldownView:
    """ This class represents the drilldown view """

    def print_drilldown(self, event, report_file):
        """ Print the drilldown view based on drilldown model """
        drilldown_model = DrilldownModel()
        ui_binmodule_list = drilldown_model.create_drilldown_model(report_file)

        title = "Drilldown for event: " + event
        border = self.__get_border(title)
        self.__print_logo(title, border)

        for ui_binmodule in ui_binmodule_list:
            print ui_binmodule.get_text()
            for ui_symbol in ui_binmodule.get_symbols_list():
                print TABULATION + ui_symbol.get_text()
                for ui_sample in ui_symbol.get_samples_list():
                    print TABULATION + TABULATION + ui_sample.get_text()
            if ui_binmodule is not ui_binmodule_list[-1]:
                print ""
        print border + "\n"

    def __print_logo(self, title, border):
        """ Print the drilldown logo """
        print "\n\n"
        print border
        print title
        print border

    def __get_border(self, title):
        """ Get the border """
        return "=" * len(title)
