#!/usr/bin/env python
# -*- coding: utf-8 -*- #
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
""" JDL Command line choice. This is where the jdl tags are printed and selected."""

import os
import sys

Rows, Columns = map(int, os.popen('stty size', 'r').read().split())


def PrintMultipleItems(items, column=Columns, filler=' '):
    """Returns a string from the items list given a character limit"""
    ni = len(items)
    per_item = int(column*1.0/ni)
    new_items = map(lambda x: x.ljust(per_item, filler)[:(per_item-1)], items)
    line = " ".join(new_items)
    return line


def JDL_PrintFunction(string2print, **kwdict):
    """Simple Print Function, in case it is needed to write to a file,
    to a variable or suspend printing.
    """
    if kwdict.get('err', False):
        print "Error: ",
    print string2print
    return


def DecryptSelection(selection):
    """    When a string is given as input eg "a,b,c" it decrypts it to
    set([a,b,c]), while a string as "1,11,3-8" to set([1,11,3,4,5,6,7,8])
     """
    if type(selection) in (type("string"), ):
        selection = selection.split(',')
        ret = []
        for i, lin in enumerate(selection):
            if '-' in lin:
                l = map(int, lin.split("-"))
                ran = range(l[0], l[1]+1)
            else:
                ran = [int(lin)]
            ret += ran
        return set(ret)
    elif type(selection) in (type([1, 2]), type((1, 2)), type(set([1, 2]))):
        return set(selection)
    else:
        return set([])


def JDL_Choice(Cdict, Order=None, start=1, selection=None, \
               PrintFunction=JDL_PrintFunction):
    """Takes care of printing the list, selections \
        and returning the results.

    JDL_Choice(Cdict, Order=None, start=1, selection=None, \
                       PrintFunction=JDL_PrintFunction)

    Cdict: (dict) with the desired values
    Order: (list, tuple) contains the keys in the order to be printed
    start: (int) the number to start counting
    selection: (list) Contains a list of integer, those preselected
    JDL_PrintFunction: (function) simple print function, in case it is \
            needed to write to a file, to a variable or suspend printing
    """
    Rows, Columns = map(int, os.popen('stty size', 'r').read().split())
    isdict = False
    if PrintFunction == None:
        PrintFunction = lambda x, **kwdict: 0
    Ckeys = Cdict.keys()
    if type(Cdict[Ckeys[0]]) == type({}):
        isdict = True
    if Order == None:
        Order = sorted(Ckeys)
    if isdict:
        # Print the headers of the dict (eg "Application Specific")
        # and a trailing underline according to their size
        underline = map(lambda x: '_'*(len(x)+2), Order)
        PrintFunction(PrintMultipleItems(Order, column=Columns))
        PrintFunction(PrintMultipleItems(underline, column=Columns))
        # Given the selected numbers from the list,
        # -- NumberingValues should return the values of the selection
        NumberingValues = {}
        # -- TextColumns is used to number and print the list of options
        TextColumns = []
        N = start
        for in_dict in Order:
            # Sort printed keys in an alphabetical order
            in_keys = sorted(Cdict[in_dict].keys())
            # Values of keys in an alphabetical order
            Values = map(lambda x: Cdict[in_dict][x], in_keys)
            Range = range(N, len(in_keys)+N)
            Values = zip(*(Range, Values))
            NumberingValues.update(dict(Values))
            TextColumn = zip(*(Range, in_keys))
            TextColumns += [TextColumn]
            N = Range[-1]+1

        # The following is used to fill the PRows list with empty keys
        # in the likely case when the Menu has unequal lengths
        Rows = map(len, TextColumns)
        dRows = max(Rows) - min(Rows) + 1
        TextColumns = map(lambda x: x + [('', '')]*dRows, TextColumns)
        TextColumns = zip(*TextColumns)
        PRows = map(lambda x: map(lambda p: "%s : %s"%p*(p[0] !=''), x), \
                    TextColumns)
        # Print the menu within the limits of the console
        for pr in PRows:
            PrintFunction(PrintMultipleItems(pr, column=Columns))
        try:
            # Get the user selection string
            if selection == None:
                PrintFunction('---------------------------------------')
                PrintFunction('0 : make it a full JDL Template')
                PrintFunction(', : for multiple selection')
                PrintFunction('- : for range selection')
                PrintFunction('q : quit')
                PrintFunction('---------------------------------------')
                try:
                    selection = \
                            raw_input('Please select from the list above: ')
                    PrintFunction('')
                except:
                    selection ='q'
                if selection =='q':
                    sys.exit()
            SetSelection = DecryptSelection(selection)
            SetNV = set(NumberingValues.keys())
            FalseInput = SetSelection - SetNV
            TrueInput = list(SetSelection & SetNV)
            ret = (map(lambda x: NumberingValues[x], TrueInput), FalseInput)
            return ret
        except ValueError:
            PrintFunction("Wrong option", err=True)
            return JDL_Choice(Cdict, Order=Order, start=start, \
                                PrintFunction=PrintFunction)
    else:
        Cdict2 = {}
        Cdict2[''] = Cdict
        return JDL_Choice(Cdict2, start=start)
        # return "81: Wrong Input!\n"
