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


class BinModule:
    """ Class to hold both binary and module tags """
    def __init__(self, name, count, symbol_list):
        self.name = name
        self.count = count
        self.symbol_list = symbol_list

    def get_name(self):
        return self.name

    def get_count(self):
        return self.count

    def get_symbol_list(self):
        return self.symbol_list


class Symbol:
    """ Class to hold symbol tag """
    def __init__(self, idref, count, symboldata):
        # The 'idref' reference the 'i' from SymbolData class
        self.idref = idref
        self.count = count
        self.symboldata = symboldata

    def get_idref(self):
        return self.idref

    def get_count(self):
        return self.count

    def get_symboldata(self):
        return self.symboldata

    def __eq__(self, other):
        """ Objects of this class are equals if
        the idref attribute of both objects are equal """
        return self.idref == other.idref


class SymbolData:
    """ Class to hold symboldata tag """
    def __init__(self, i, name, file_name, line, symboldetails):
        # The 'i' from this class reference the 'i' from
        # SymbolDetails class
        self.i = i
        self.name = name
        self.file_name = file_name
        self.line = line
        self.symboldetails = symboldetails

    def get_id(self):
        return self.i

    def get_name(self):
        return self.name

    def get_file_name(self):
        return self.file_name

    def get_line(self):
        return self.line

    def get_symboldetails(self):
        return self.symboldetails


class SymbolDetails:
    """ Class to hold symboldetais tag """
    def __init__(self, i, detaildata_list):
        self.i = i
        self.detaildata_list = detaildata_list

    def get_id(self):
        return self.i

    def get_detaildata_list(self):
        return self.detaildata_list


class DetailData:
    """ Class to hold detaildata tag """
    def __init__(self, line, count):
        self.line = line
        self.count = count

    def get_line(self):
        return self.line

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def __eq__(self, other):
        """ Objects of this class are equals if
        the line attribute of both objects are equal """
        return self.line == other.line
