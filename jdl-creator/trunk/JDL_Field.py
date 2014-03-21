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
"""JDL_Field instance."""
import glob

os = glob.os

NotExclusiveFields = tuple()
OrderToShow = tuple()


class JDL_Field(object):
    """JDL Field instance.
    JDL_Field(field='#', value='#', tag=tuple(), comment='', \
                 JDL_tag=None)
    """

    def __init__(self, field='#', value='#', tag=tuple(), comment='', \
                 JDL_tag=None):
        """ Ctor. Accepts the field's name (string), the model value corresponding
        the specified field, according to the option, a tuple of tags, a comment (optional)
        and a JDL_tag (that is optional). If the JDL_tag is None, it is given a value.
        Initializes the values of self.JDL and self.tags.
        If the JDL_tag is not None, then self.JDL = JDL_tag
        """
        # DEBUGGING:
        # Until now:
        #     1. JDL_Field(self, field, tag, comment)
        #     2. JDL_Field(JDL_tag)
        if JDL_tag == None:
            self.JDL = {} # initialization to empty dictionary
            # self.JDL is a dictionary of one record, with key=field and value={key:value}
            # DEBUGGING:
            # Strange implementation. Check later for reason why it's implemented that way.
            # print "printing tag accepted for "
            # DEBUGGING:
            # print field
            # print tag
            self.tags = map(lambda x: x.upper(), tag) # capitalizes the elements of the tag taken as arg
            # print "printing tag after map"
            # DEBUGGING:
            # print self.tags
            field = field.strip() # deletes all the whitespaces from the front and the end of the field string
            self.JDL[field] = {}
            jdl_field = self.JDL[field]
            jdl_field['value'] = [value.strip()]
            jdl_field['tag'] = map(lambda x: x.upper(), tag)
            jdl_field['comment'] = [comment.strip()]
            # DEBUGGING:
            # print "Printing the JDL"
            # print self.JDL
        else:
            # JDL_tag has different structure from self.JDL.
            # JDL_tag is a list with:
            # JDL_tag[0] --> self.JDL
            # JDL_tag[1] --> self.tags
            self.JDL = JDL_tag[0]
            self.tags = JDL_tag[1]
        pass

    def __add__(self, jdl2add):
        """It Joins the j1.JDL and j2.JDL dictionaries."""
        JDL_new = self.JDL.copy()
        tags_new = self.tags + jdl2add.tags
        for field, contents in jdl2add.JDL.items():
            if field not in JDL_new:
                JDL_new[field] = contents
            else:
                for value_tag_comment, itm in jdl2add.JDL[field].items():
                    # DEBUGGING:
                    # print value_tag_comment
                    # print itm
                    JDL_new[field][value_tag_comment] += itm
                    # print JDL_new[field]
        return JDL_Field(JDL_tag=[JDL_new, tags_new])

    def __GetConflictingTags(self):
        """Returns the tags that are conflicting"""
        ret = []
        for tag in set(self.tags):
            if tag and self.tags.count(tag) > 1:
                print tag
                ret += [tag]
        return ret

    def __GetConflictingFields(self):
        """Returns the fields that are conflicting"""
        ret = []
        for field, item in self.JDL.items():
            values = item['value']
            if (len(set(values)) > 1) and (field not in NotExclusiveFields):
                ret += [field]
        return ret

    def hasConflicts(self):
        """If there are conflicts, this function will find them."""
        hC = len(self.__GetConflictingFields())
        hC += len(self.__GetConflictingTags())
        return hC>0

    def getConflictString(self):
        """If there are conflicts, the string to print will be returned"""
        ConflTags = self.__GetConflictingTags()
        ConflFields = list(set(self.__GetConflictingFields()))
        ret = [""]
        if (len(ConflTags) > 0) or (len(ConflFields) > 0):
            ret += ['# ** Conflict, not a valid JDL! **\n']
        if len(ConflTags) > 1:
            ret += ['# ** %s are defined multiple times.\n' \
                        %(", ".join(ConflTags), )]
        elif ConflTags:
            ret += ['# ** %s is defined multiple times.\n'\
                        %(ConflTags[0], )]
        if len(ConflFields) > 1:
            ret += ['# ** The fields %s are defined multiple times.\n'\
                        %(", ".join(ConflFields), )]
        elif ConflFields:
            ret += ['# ** The field %s is defined multiple times.\n'\
                        %(ConflFields[0], )]
        return "".join(ret)

    def __GetOkFields(self):
        """Fields that are ok."""
        AllFields = set(self.JDL.keys())
        ConflFields = set(self.__GetConflictingFields())
        OkFields = AllFields - ConflFields
        return OkFields

    def __print_field_dict(self, field_name, field_dict, separate=False):
        """Gets the field and its' dict and prints it in a JDL Format"""
        if separate:
            ret = []
            values = field_dict['value']
            comments = field_dict['comment']
            for iv, value in enumerate(values):
                coms = comments[iv]
                if coms:
                    coms = '# ' + coms
                ret += ["%s = %s; %s\n"%(field_name, value, coms)]
            ret = "".join(set(ret))
        else:
            values = list(set(field_dict['value']))
            comments = list(set(field_dict['comment']))
            vals = "\n\t&& ".join(values)
            coms= "".join(comments)
            if coms:
                coms = "\n# " + " // ".join(comments)
            ret = "%s = %s; %s\n"%(field_name, vals, coms)
        # print field_name, field_dict, separate, ret
        return ret

    def __MakeJDL(self):
        """The main jdl create function"""
        ConflTags = self.__GetConflictingTags()
        ConflFields = list(set(self.__GetConflictingFields()))
        OkFields = list(set(self.__GetOkFields()))
        ret = [self.getConflictString()]
        for field in OrderToShow:
            if field in OkFields:
                ret += [self.__print_field_dict(field, self.JDL[field])]
                OkFields.remove(field)
            elif field in ConflFields:
                ret += [self.__print_field_dict(field, self.JDL[field], \
                        separate=True)]
                ConflFields.remove(field)
        for field in sorted(OkFields):
            ret += [self.__print_field_dict(field, self.JDL[field])]
        for field in sorted(ConflFields):
            ret += [self.__print_field_dict(field, self.JDL[field], \
                        separate=True)]
        return "".join(ret)[:-1]

    def __str__(self):
        return self.__MakeJDL()

    def __repr__(self):
        return "JDL_Field instance, Fields >> %s"%(" - ".join(self.JDL.keys()))


def MakeList(SList, joiner='", "'):
    """docstring for MakeList"""
    return '{"' + joiner.join(SList) + '"}'


def SmartJDL():
    """docstring for SmartJDL"""
    ListSet = lambda f: list(set(f))
    FindFiles = lambda f: set(glob.glob(f))
    IsExecutable = lambda f: os.access(f, os.X_OK) and (not os.path.isdir(f))
    IsLessThan1MB = lambda f: os.path.getsize(f) < 1024**2.0
    OpenRead = lambda f: open(f, 'r').read()
    FindFileWith = lambda name, List: filter(lambda x: name in x, List)[0]
    AllFiles = set(filter(lambda f: (not os.path.isdir(f)), FindFiles('*')))
    Executable = 'run.sh'
    # Find the files that might be needed
    JDLs = FindFiles('*[jJ][dD][lL]')
    TXTs = FindFiles('*[tT][xX][tT]')
    TGZs = FindFiles('*[tT][aA][rR].[gGbB][zZ]') | FindFiles('*[tT][gGbB][zZ]')
    DATs = FindFiles('*[dD][aA][tT]')
    SHs = FindFiles('*[sS][hH]')
    EXEs = FindFiles('*[eE][xX][eE]') | set(filter(IsExecutable, AllFiles))
    InboxList = (TXTs | DATs | SHs | EXEs | TGZs) - JDLs
    #  Search in files or control files, within the rational limits,
    # therefore exclude searching into files larger than 1MB
    # files that might be needed.
    MassiveText = "".join(map(OpenRead, filter(IsLessThan1MB, AllFiles-JDLs)))
    FilesToCycle = (AllFiles-InboxList-JDLs)
    # print FilesToCycle, MassiveText
    InboxList = InboxList|set(filter(lambda f: f in MassiveText, FilesToCycle))
    #  Search for the executable, with preferences
    if SHs:
        if len(SHs) == 1:
            Executable = SHs.pop()
        else:
            text = "".join(SHs)
            if 'run' in text:
                Executable = FindFileWith('run', SHs)
            elif 'mpi-start-wrapper' in text:
                Executable = FindFileWith('mpi-start-wrapper', SHs)
            elif 'namd' in text:
                Executable = FindFileWith('namd', SHs)
            elif 'vasp' in text:
                Executable = FindFileWith('vasp', SHs)
            elif 'wrf' in text:
                Executable = FindFileWith('wrf', SHs)
            else:
                Executable = SHs.pop()
    elif EXEs:
        if len(EXEs) == 1:
            Executable = EXEs.pop()
        else:
            text = "".join(EXEs)
            if 'namd' in text:
                Executable = FindFileWith('namd', EXEs)
            elif 'vasp' in text:
                Executable = FindFileWith('vasp', EXEs)
            elif 'wrf' in text:
                Executable = FindFileWith('wrf', EXEs)
            else:
                Executable = EXEs.pop()
    Executable = '\"' + Executable + '\"'
    return Executable, MakeList(InboxList)


def Smarten(jfield):
    """docstring for fname"""
    Executable, InputSandbox = SmartJDL()
    # OutputSandbox not used
    OutputSandbox = '{"std.err","std.out","folder.tar.gz"}'
    OutputSandboxComment = 'folder.tar.gz was added to your OutputSandbox. Use "tar -cvfz folder.tar.gz *.dat" to tar all your files and "tar -xvfz folder.tar.gz" to untar'
    
    if jfield.JDL.has_key('InputSandbox'):
        IS = JDL_Field('InputSandbox', InputSandbox)
        if len(jfield.JDL['InputSandbox']['value']) == 1:
            jfield.JDL.update(IS.JDL)
        else:
            jfield = jfield + JDL_Field('InputSandbox', InputSandbox)
    if jfield.JDL.has_key('Executable'):
        IS = JDL_Field('Executable', Executable)
        if len(jfield.JDL['Executable']['value']) == 1:
            jfield.JDL.update(IS.JDL)
        else:
            jfield = jfield + JDL_Field('Executable', Executable)
    # if jfield.JDL.has_key('OutputSandbox'):
    #     IS = JDL_Field('OutputSandbox', OutputSandbox, comment=OutputSandboxComment)
    #     if len(jfield.JDL['OutputSandbox']['value']) == 1:
    #         jfield.JDL.update(IS.JDL)
    #     else:
    #         jfield = jfield + JDL_Field('OutputSandbox', OutputSandbox)
    return jfield
