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

%define gcj_support	1

Name:		junit
Version:	3.8.2
Release:	%mkrel 7
Summary:	Java regression test package
License:	CPL
Url:		http://www.junit.org/
Group:		Development/Java
Source0:	http://osdn.dl.sourceforge.net/junit/junit3.8.2.tar.bz2
Source1:	junit3.8.2-build.xml
Source2:	http://repo1.maven.org/maven2/junit/junit/3.8.2/junit-3.8.2.pom
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.6
%if %{gcj_support} 	 
BuildRequires:	java-gcj-compat-devel 	 
%else 	 
BuildArch:      noarch
%endif
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
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name} 	 
# pom 	 
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms 	 
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr %{name}%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}
# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/demo/junit
cp -pr %{name}%{version}/%{name}/* %{buildroot}%{_datadir}/%{name}/demo/junit

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# fix end-of-line 	 
%{__perl} -pi -e 's/\r\n/\n/g' README.html

for i in `find %{name}%{version}/doc -type f -name "*.htm*"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done 	 

for i in `find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name "*.java"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

install -d -m 755 %{buildroot}%{_docdir}/%{name}
cp -p README.html %{buildroot}%{_docdir}/%{name}
cp -par doc/* %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post 	 
%update_maven_depmap 	 
%if %{gcj_support}
%{update_gcjdb} 	 
%endif 	 

%postun 	 
%update_maven_depmap 	 
%if %{gcj_support} 	 
%{clean_gcjdb} 	 
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.html
%{_datadir}/maven2
%{_mavendepmapfragdir}
%if %{gcj_support}
%{_libdir}/gcj/%{name} 	 
%endif

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%exclude %{_docdir}/%{name}/README.html

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}
