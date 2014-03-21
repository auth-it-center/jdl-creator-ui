Summary: JDL Template Creator
Name: jdl-creator
Version: 0.2
Release: 7%{?dist}
License: GPL
Group: Development/Tools
URL: http://code.grid.auth.gr/jdl-creator
BuildArch: noarch
Source0: jdl-creator
Source1: JDL_Choise.py
Source2: JDL_ControlFile.py
Source3: JDL_Field.py
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python
Requires: python
Prefix: /usr

%description
Installs jdl-creator script and necessary libraries

%prep
cp %{SOURCE0} .
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build 


%install
rm -fr ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{prefix}
mkdir ${RPM_BUILD_ROOT}%{prefix}/bin 
mkdir -p ${RPM_BUILD_ROOT}%{prefix}/lib64/python2.4

cp jdl-creator ${RPM_BUILD_ROOT}%{prefix}/bin/
cp *.py ${RPM_BUILD_ROOT}%{prefix}/lib64/python2.4/


%clean
rm -fr ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,-)
%{prefix}/bin/jdl-creator
%{prefix}/lib64/python2.4/*


%changelog
* Fri Jan 10 2014 Stefanos Laskaridis <laskstef@grid.auth.gr> 0.2-7
- Changed requirements for CUDA. Deleted "Environment = {"NODES_REQ=1:cuda"};". Changed from "Requirements = Member("CUDA", other.GlueHostApplicationSoftwareRunTimeEnvironment);" to "Requirements = Member("GPU", other.GlueHostApplicationSoftwareRunTimeEnvironment);"
* Fri Apr 05 2013 Georgia Tsiamanta <gtsiaman@grid.auth.gr> 0.2-4
- Replace "ce01.grid.auth.gr" with "cream01.grid.auth.gr"
* Mon May 21 2012 Paschalis Korosoglou <pkoro@grid.auth.gr> 0.2-3
- Correction in comment
* Tue Jun 16 2010 Lampros Mountrakis <lmount@grid.auth.gr> 0.1-3
- Renamed the module files and added the "--smart" feature
* Tue Jun 11 2010 Lampros Mountrakis <lmount@grid.auth.gr> 0.1-2
- Documentation added to the source and made it more user-friendly
* Tue Jun 08 2010 Paschalis Korosoglou <pkoro@grid.auth.gr> 0.0.1-1
- Initial package version and release
