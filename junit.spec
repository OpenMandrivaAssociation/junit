# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:		junit
Version:	3.8.2
Release:	%mkrel 6
Summary:	Java regression test package
License:	CPL
Url:		http://www.junit.org/
Group:		Development/Java
Source0:	http://osdn.dl.sourceforge.net/junit/junit3.8.2.tar.bz2
Source1:	junit3.8.2-build.xml
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.6
BuildArch:      noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JUnit is a regression testing framework written by Erich Gamma and Kent
Beck. It is used by the developer who implements unit tests in Java.
JUnit is Open Source Software, released under the IBM Public License and
hosted on SourceForge.

%package manual
Group:		Development/Java
Summary:	Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:		Development/Java
Summary:	Demos for %{name}
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}%{version}
# extract sources
%{jar} xf src.jar
rm -f src.jar
cp %{SOURCE1} build.xml

%build
%ant dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}%{version}/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr %{name}%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}
# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/demo/junit
cp -pr %{name}%{version}/%{name}/* %{buildroot}%{_datadir}/%{name}/demo/junit

install -d -m 755 %{buildroot}%{_docdir}/%{name}
cp -p README.html %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc %dir %{name}
%doc %{_docdir}/%{name}/README.html

%files manual
%defattr(-,root,root,-)
%doc %{name}%{version}/doc

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}
