# -*- coding: utf-8 -*-

"""
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
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

from decimal import Decimal
import cpi.drilldown.opreport_parser as opreport_parser


class DrilldownModel():
    """ Class to create the model of drilldown """
    def __init__(self):
        self.binmodule_list = []

    def create_drilldown_model(self, report_file):
        """ Create the drilldown model object and return it """
        parser = opreport_parser.OpreportParser()
        self.binmodule_list = parser.parse(report_file)

        binmodule_total_count = self.get_binmodule_total_count()
        ui_binmodule_list = []

        # Create drilldown model objects
        for binmodule in self.binmodule_list:
            # Create UiBinModule
            binmodule_percent = self.calc_percentage(binmodule.get_count(),
                                                     binmodule_total_count)
            # Do not add when count is zero
            if binmodule.get_count() == 0:
                continue
            ui_binmodule = UiBinModule(binmodule.get_name(), binmodule_percent)
            ui_binmodule_list.append(ui_binmodule)

            for symbol in binmodule.get_symbol_list():
                symbol_count = symbol.get_count()
                symboldata = symbol.get_symboldata()
                # Create UiSymbol
                symbol_percent = self.calc_percentage(symbol_count,
                                                      binmodule_total_count)
                ui_symbol = UiSymbol(symboldata.get_name(),
                                     symboldata.get_file_name(),
                                     symbol_percent)
                ui_binmodule.add_symbol(ui_symbol)

                symboldetails = symboldata.get_symboldetails()
                for ddata in symboldetails.get_detaildata_list():
                    # Create UiSample
                    sample_percent = self.calc_percentage(ddata.get_count(),
                                                          symbol_count,
                                                          symbol_percent)
                    # Do not add when line is zero
                    if ddata.get_line() == "0":
                        continue
                    ui_sample = UiSample(ddata.get_line(), sample_percent)
                    ui_symbol.add_sample(ui_sample)
        ui_binmodule_list.sort()
        return ui_binmodule_list

    def get_binmodule_total_count(self):
        """ Get the total count from binary and modules """
        count = 0
        for binmodule in self.binmodule_list:
            count += binmodule.get_count()
        return count

    @staticmethod
    def calc_percentage(count, total_count, percent_factor=100):
        """ Calculate the percentage for a specific count
        in proportion to the total, using the percent factor """
        percentage = Decimal(float(count) * float(percent_factor) / total_count)
        percentage = round(percentage, 2)
        return percentage


class UiBinModule():
    """ Class to hold info about the binary that was profiled """
    def __init__(self, name, percentage):
        self.name = name
        self.percentage = percentage
        self.symbols_list = []

    def get_symbols_list(self):
        """ Get a list of symbols that are part of this binary/module """
        return self.symbols_list

    def add_symbol(self, symbol):
        """ Add a new symbol to the list and sort it """
        self.symbols_list.append(symbol)
        self.symbols_list.sort()

    def get_text(self):
        """ Get formatted text to be used in UI """
        # If percentage is zero, round it
        if self.percentage == 0:
            self.percentage = str("< 0.01")
        text = str(self.percentage) + "% in " + self.name
        return text

    def get_percentage(self):
        """ Get the bin/module percentage """
        return self.percentage

    def __lt__(self, other):
        """ Sort list ascending by percentage """
        return self.percentage > other.percentage


class UiSymbol():
    """ Class to hold info about symbols """
    def __init__(self, name, file_name, percentage):
        self.name = name
        self.file_name = file_name
        self.percentage = percentage
        self.samples_list = []

    def get_samples_list(self):
        """ Get a list of samples that are part of this symbol """
        return self.samples_list

    def add_sample(self, sample):
        """ Add a new sample to the list and sort it """
        self.samples_list.append(sample)
        self.samples_list.sort()

    def get_text(self):
        """ Get formatted text to be used in UI """
        # If percentage is zero, round it
        if self.percentage == 0:
            self.percentage = str("< 0.01")
        text = str(self.percentage) + "% in " + self.name
        text += " [" + self.file_name + "]"
        return text

    def get_percentage(self):
        """ Get the symbol percentage """
        return self.percentage

    def __lt__(self, other):
        """ Sort list ascending by percentage """
        return self.percentage > other.percentage


class UiSample():
    """ Class to hold info about samples """
    def __init__(self, line, percentage):
        self.line = line
        self.percentage = percentage

    def get_text(self):
        """ Get formatted text to be used in UI """
        # If percentage is zero, round it
        if self.percentage == 0:
            self.percentage = str("< 0.01")
        text = str(self.percentage) + "% on line " + self.line
        return text

    def __lt__(self, other):
        """ Sort list ascending by percentage """
        return self.percentage > other.percentage
