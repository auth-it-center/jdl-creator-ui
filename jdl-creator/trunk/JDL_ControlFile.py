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
""" JDL Control file """


import JDL_Field as jf
JDL_Field = jf.JDL_Field
Smarten = jf.Smarten
# If you want to add more field, first you have to give them a unique name
# in the JDL_List dictionary matching the other field and then add it
# to the Menu you would like it to be presented.
#
# For NotExclusiveFields and OrderToShow see "jdl_field.py"

jf.NotExclusiveFields = ('Requirements', )
jf.OrderToShow = ('JobType', 'Executable', 'Arguments', 'CpuNumber', 'StdOutput', \
                  'StdError', 'InputSandbox', 'OutputSandbox', 'Environment', 'Requirements')

# A Dictionary containing selection and text to be added in the .jdl file.
JDL_List = {
        # 'NormalJob': JDL_Field('JobType','"Normal"'),
        # 'JobType MPICH': JDL_Field('JobType','"MPICH"', tag=['MPI', 'MPICH']),
        # 'JobType MPICH2': JDL_Field('JobType','"MPICH2"', tag=['MPI', 'MPICH2']),
        # 'JobType OPENMPI': JDL_Field('JobType','"OPENMPI"', tag=['MPI', 'OPENMPI']),
        'Parametric-step' : JDL_Field('JobType','"Parametric"') + JDL_Field('Arguments','"_PARAM_"') + \
         JDL_Field('Parameters','6') + JDL_Field('ParameterStep','2') + JDL_Field('ParameterStart','0'),
        'Parametric-list' : JDL_Field('JobType','"Parametric"') + JDL_Field('Arguments','"_PARAM_"') + \
         JDL_Field('Parameters','{2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0}'),
        'Arguments': JDL_Field('Arguments','"arg1 arg2"'),
        'RetryCount': JDL_Field('RetryCount','7'),
        'ShallowRetryCount': JDL_Field('ShallowRetryCount','7'),
        'StdError': JDL_Field('StdError','"std.err"'),
        'StdOutput': JDL_Field('StdOutput','"std.out"'),
        'OutputSandbox': JDL_Field('OutputSandbox','{"std.err","std.out"}'),
        'InputSandbox': JDL_Field('InputSandbox','{"run.sh", "data.dat"}'),
        'Executable': JDL_Field('Executable','"run.sh"'),

        'CpuNumber': JDL_Field('CpuNumber','8'),
        'CUDA': JDL_Field('Requirements','Member("GPU", other.GlueHostApplicationSoftwareRunTimeEnvironment)'),
        'MaxWallClockTime': JDL_Field('Requirements','(other.GlueCEPolicyMaxWallClockTime >= 168)',\
                                      comment='Time is in hours'),
        'RAM_Size': JDL_Field('Requirements','(other.GlueHostMainMemoryRAMSize >= 1024)', comment='RAM size is in MB'),
        'x86_64': JDL_Field('Requirements','(other.GlueHostArchitecturePlatformType == "x86_64")'),
        'ScientificLinux5': JDL_Field('Requirements','(other.GlueHostOperatingSystemRelease >= 5.0 && other.GlueHostOperatingSystemRelease < 6.0)', tag=['OS']),
        'ScientificLinux4': JDL_Field('Requirements','(other.GlueHostOperatingSystemRelease >= 4.0 && other.GlueHostOperatingSystemRelease < 5.0)', tag=['OS']),
        'OPENMP': JDL_Field('Environment','{"OPENMP=true"}') + JDL_Field('CpuNumber','8'),
        'MPICH': JDL_Field('Requirements','Member("MPICH", other.GlueHostApplicationSoftwareRunTimeEnvironment)', tag=['MPICH','MPI']) + JDL_Field('CpuNumber','8'),
        'MPICH2': JDL_Field('Requirements','Member("MPICH2", other.GlueHostApplicationSoftwareRunTimeEnvironment)', tag=['MPICH2','MPI']) + JDL_Field('CpuNumber','8'),
        'OPENMPI': JDL_Field('Requirements','Member("OPENMPI", other.GlueHostApplicationSoftwareRunTimeEnvironment)', tag=['OPENMPI','MPI']) + JDL_Field('CpuNumber','8'),
        'MPI-Start': JDL_Field('Requirements','Member("MPI-START", other.GlueHostApplicationSoftwareRunTimeEnvironment)') + JDL_Field('Arguments','"MPICH solver.exe"'),

        'hugemem': JDL_Field('Environment','{"NODES_REQ=1:ppn=8:hugemem"}') + JDL_Field('Requirements','(other.GlueCEInfoHostName == "cream01.grid.auth.gr")', tag=['CE']),
        'NODES_REQ': JDL_Field('Environment','{"NODES_REQ=2:ppn=2"}'),
        'HYDRA': JDL_Field('Requirements','Member("HYDRA-CLIENT", other.GlueHostApplicationSoftwareRunTimeEnvironment)'),
        'GR-01-AUTH': JDL_Field('Requirements','(other.GlueCEInfoHostName == "cream01.grid.auth.gr")', tag=['CE']),
        'HG-03-AUTH': JDL_Field('Requirements','(other.GlueCEInfoHostName == "cream.afroditi.hellasgrid.gr")', tag=['CE']),
        'CE-Regex': JDL_Field('Requirements','RegExp("cream.afroditi.hellasgrid.gr",other.GlueCEUniqueId)', tag=['CE']),
        'Perusal' : JDL_Field('PerusalFileEnable','true') + JDL_Field('PerusalTimeInterval','1800', comment='Time is in seconds'),

}

default_jdl =  JDL_List['Executable'] + JDL_List['StdOutput'] + JDL_List['StdError'] + \
               JDL_List['InputSandbox'] + JDL_List['OutputSandbox']


# Menu is a dictionary with key = category and value = list of Arguments
Menu = {
    'a) JobTypes and Standard Job Fields:': [
        'Parametric-step' ,
        'Parametric-list' ,
        'Arguments',
        'RetryCount',
        'ShallowRetryCount',
        'StdError',
        'StdOutput',
        'OutputSandbox',
        'InputSandbox',
        'Executable',
    ],

    'b) Application Specific:': [
        'CpuNumber',
        'CUDA',
        'MaxWallClockTime',
        'RAM_Size',
        'x86_64',
        'ScientificLinux5',
        'ScientificLinux4',
        'OPENMP',
        'MPICH',
        'MPICH2',
        'OPENMPI',
        'MPI-Start',
    ],

    'c) Miscellaneous:':[
        'hugemem',
        'NODES_REQ',
        'HYDRA',
        'GR-01-AUTH',
        'HG-03-AUTH',
        'CE-Regex',
        'Perusal' ,
    ],

}

