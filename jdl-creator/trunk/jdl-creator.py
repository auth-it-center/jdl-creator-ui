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
""" Generate simple JDL Templates """

__author__ = "Lampros Mountrakis, lmount@grid.auth.gr"

__version__ = "0.1 Beta"

__desciption__ = "Simple JDL Template creator"

import os
import sys
from JDL_ControlFile import *
from JDL_Choice import *
from optparse import OptionParser
from bcolours import *


def MakeArgList(Menu, JDL_List):
    """Converts the Menu to include the JDL_List values as well"""
    NewDict = Menu.copy()
    for lst in Menu:
        NewDict[lst] = {}
        for ils in Menu[lst]:
            NewDict[lst][ils] = JDL_List[ils]
    return NewDict


def Add_JDL_Fields(ListOfJDLFields):
    """Returns the sum of a JDL_Field List"""
    Summaray = ListOfJDLFields[0]
    for CCS in ListOfJDLFields[1:]:
        Summaray = Summaray + CCS
    return Summaray


def ParseArguments():
    """Parses the arguments from the command line"""
    # available arguments
    # 1. -o output to specific file
    # 2. -m create jdl file
    # 3. -a arguments for printing the resulting jdl immediately
    # 4. -f force output
    # 5. -q quiet
    # 6. -s smart
    # 7. -l list options
    # 8. -e examples

    description = __desciption__ +\
        "For bug reporting you can contact us at support@grid.auth.gr"
    usage = "usage: %prog [options] [arguments]"

    parser = OptionParser(version="%prog " + __version__, \
            description=description, usage=usage)

    parser.add_option("-o", "--output", dest="filename", \
                      help="save the output to FILE", metavar="FILE")
    parser.add_option("-m", "--make-jdl", \
                      action="store_true", dest="make_jdl", default=False, \
                      help="make the output a full JDL template")
    parser.add_option("-a", "--arguments", help="options to choose",  \
            type="string", metavar="field/s", default='', dest="arguments")
    parser.add_option("-f", "--force", \
                      action="store_true", dest="force", default=False, \
                      help="force the output, even if there are conflicts")
    parser.add_option("-q", "--quiet", \
                      action="store_true", dest="quiet", default=False, \
                      help="supress the output")
    parser.add_option("-s", "--smart", \
                    action="store_true", dest="smart", default=False, \
                    help="will try identify the Executable and InputSandbox")
    parser.add_option("-l", "--list", \
                      action="store_true", dest="list_option", default=False, \
                      help="list all the available fields")
    parser.add_option("-e", "--examples", \
                      action="store_true", dest="examples", default=False, \
                      help="show some examples of use.")
    return parser.parse_args() # you are telling the OptionParser to parse the arguments.
    # returns a dictionary with key = dest, value = default (if no arguments are passed


def ShowExamples(prog, user, hostn):
    """Prints a list of examples when opening with arg -e"""
    # (user and hostname do not seem to work
    # change output to discriminate between command and output
    print "printing locals"
    print locals()
    startingPoint = "[%(user)s@%(hostn)s]$"%locals()
    startingPoint = "\n\t$"%locals()
    print '\nusage: %s [options] [arguments]\n\nEXAMPLES'%(prog, )

    myargs = "--make-jdl -o jdlfile.jdl"
    print '%(startingPoint)s %(prog)s %(myargs)s'%locals()
    print bcolors.OKGREEN + '\t\t Simple JDL and the output is saved to "jdlfile.jdl". ' + bcolors.ENDC

    myargs = "--arguments MPI-MPICH,x86_64,ScientificLinux5"
    print '%(startingPoint)s %(prog)s %(myargs)s'%locals()
    print bcolors.OKGREEN +'\t\t MPICH JDL asking for x64 architecture and SL5.' + bcolors.ENDC

    myargs = "-m -a MPI-MPICH,x86_64,ScientificLinux5 -o MyJDL.jdl"
    print '%(startingPoint)s %(prog)s %(myargs)s'%locals()
    print bcolors.OKGREEN + '\t\t Making the above a full JDL template \
    and saving it to MyJDL.jd   l.' + bcolors.ENDC

    myargs = "-m --arguments MPI-MPICH,MPI-MPICH2,MPI-Start"
    print '%(startingPoint)s %(prog)s %(myargs)s'%locals()
    print bcolors.FAIL + '\t\t MPI Conficts' + bcolors.ENDC

    myargs = "--force -m --arguments MPI-MPICH,MPI-MPICH2,MPI-Start"
    print '%(startingPoint)s %(prog)s %(myargs)s'%locals()
    print bcolors.OKBLUE + '\t\t MPI Conficts - forced' + bcolors.ENDC

    myargs = "-m -f --arguments MPI-MPICH, MPI-MPICH2, MPI-Start"
    print '%(startingPoint)s %(prog)s %(myargs)s'%locals()
    print bcolors.FAIL + '\t\t Errors due to spaces between the arguments' + bcolors.ENDC

    sys.exit()


def ArgumentDecrypt(options, args):
    """Given the parsed argument, returns a tuple containing : (arguments, args, PrintFunction,
    list_option, make-jdl, examples)"""
    # args are the arguments taken from the command line upon start of the program
    # arguments are the arguments used inside the program to make a choice
    try:
        PrintFunction = JDL_PrintFunction # the function used to print each value, defined in JDL_Choice
        list_option = options.list_option
        make_jdl = options.make_jdl
        examples = options.examples
        # if you haven't put -l
        if list_option or examples:
            return (False, args, PrintFunction, list_option, False, examples)
        # if you haven't put -q
        if options.quiet:
            PrintFunction = None
        if args: # args is the input taken from inside the jdl, when you are called to make a choice
            # DEBUGGING
            # print "args is not none"
            args = ", ".join(args)
            args = DecryptSelection(args)
            PrintFunction = None
        else:
            # DEBUGGING
            # print "args is none, of course"
            args = None
        arguments = options.arguments.split(',')

        if len(arguments) > 0 and arguments[0]: # argument[0] is force
            sum_JDL = JDL_List[arguments[0].strip()]
            for argmnt in arguments[1:]:
                sum_JDL = sum_JDL + JDL_List[argmnt.strip()]
            arguments = sum_JDL
            if not args:
                PrintFunction = None
                args = [44]
        else:
            arguments = None
        ret = (arguments, args, PrintFunction, list_option, make_jdl, examples)
        return ret
    except:
        print "58: Invalid Arguments."
        sys.exit()


def main():
    """Parse the arguments, get the field, give the appropriate output"""
    ArgList = MakeArgList(Menu, JDL_List) # both parameters are taken from JDL_ControlFile.py
    #DEBUGGING: # print Menu
    # Take the arguments accepted
    (options, args) = ParseArguments()
    # DEBUGGING:
    print "Options:"
    print options
    print "Arguments:"
    print args
    # Decrypt the arguments accepted
    (arguments, args, PrintFunction, list_option, make_jdl, examples) = \
        ArgumentDecrypt(options, args)

    print "args:"
    print args
    # Create useful environment vars
    prog = os.path.basename(sys.argv[0])
    user = os.environ.get('USER', 'user')
    hostn = os.environ.get('HOSTNAME', 'ui2').split('.')[0]

    # Execute code according to parameters taken
    if examples:
        ShowExamples(prog, user, hostn)
    if list_option:
        RealChoice, FalseInput = JDL_Choice(ArgList, selection=[44], \
                                PrintFunction=PrintFunction)
        sys.exit()

    RealChoice, FalseInput = JDL_Choice(ArgList, selection=args, \
                            PrintFunction=PrintFunction)
    if make_jdl or (0 in FalseInput):
        RealChoice = RealChoice + [default_jdl]
    if arguments:
        RealChoice = RealChoice + [arguments]
    if not RealChoice:
        print
    else:
        JDL_Summ = Add_JDL_Fields(RealChoice)
        if options.smart:
            JDL_Summ = Smarten(JDL_Summ)
        Conficts = JDL_Summ.getConflictString()
        if (not Conficts) or options.force:
            # If there is a conflict or if it is forced
            ToPrint = ''
            ToPrint = ToPrint + "# ---------------------------------------- \n"
            ToPrint = ToPrint + "# JDL Template Created by %s.\n"%(prog, )
            ToPrint = ToPrint + "# More info @(support@grid.auth.gr)\n"
            ToPrint = ToPrint + "# ---------------------------------------- \n"
            ToPrint = ToPrint + str(JDL_Summ) + "\n"
            if options.filename: # write the output into the given filename
                pyfile = open(options.filename, 'w')
                pyfile.write(ToPrint)
                pyfile.close()
            print ToPrint
        else:
        # Conflicts and not forced
            print Conficts

if __name__ == '__main__':
    main()
