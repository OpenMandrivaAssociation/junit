Name:           junit
Epoch:          1
Version:        4.13.2
Release:        1
Summary:        Java regression test package
License:        EPL-1.0
URL:            https://junit.org/junit4/
BuildArch:      noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        generate-tarball.sh

Patch1:         0001-Port-to-hamcrest-2.2.patch
Patch2:         0002-Port-to-OpenJDK-21.patch

BuildRequires:  javapackages-bootstrap

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck. 
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and 
hosted on GitHub.

%package manual
Summary:        Manual for %{name}

%description manual
Documentation for %{name}.

%prep
%autosetup -p1 -C


# InaccessibleBaseClassTest fails with Java 8
sed -i /InaccessibleBaseClassTest/d src/test/java/org/junit/tests/AllTests.java

%pom_remove_plugin :replacer
sed s/@version@/%{version}/ src/main/java/junit/runner/Version.java.template >src/main/java/junit/runner/Version.java

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

# Removing hamcrest source jar references (not available and/or necessary)
%pom_remove_plugin :maven-javadoc-plugin

%mvn_file : %{name}

%mvn_alias junit:junit junit:junit-dep

%build
%mvn_build -j -- -DjdkVersion=1.8 -P\!restrict-doclint

%install
%mvn_install

%files -f .mfiles
%license LICENSE-junit.txt
%doc README.md

%files manual
%license LICENSE-junit.txt
%doc doc/*
