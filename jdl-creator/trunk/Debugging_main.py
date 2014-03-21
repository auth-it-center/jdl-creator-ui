__author__ = 'Steve'

from JDL_Field import *
from JDL_ControlFile import *


# field1 = JDL_Field("cuda", "import cuda")
# field2 = JDL_Field("cuda2", "import cuda")
#
# print "Before"
# print field1
# print field2
#
#
# print "after"
# print field1.__add__(field2)


def MakeArgList(Menu, JDL_List):
    """Makes the Menu to JDL_Field"""
    NewDict = Menu.copy()
    for lst in Menu:
        NewDict[lst] = {}
        for ils in Menu[lst]:
            NewDict[lst][ils] = JDL_List[ils]
    print NewDict
    return NewDict


MakeArgList(Menu, JDL_List)