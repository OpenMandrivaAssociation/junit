Summary:	Java regression test package
Name:		junit
Version:	4.10
Release:	2
License:	CPL
Group:		Development/Java
Url:		http://www.junit.org/
# git clone git://github.com/KentBeck/junit.git junit.git
# cd junit
# git archive --format=tar -o junit-%version.tar --prefix junit-%version/ r%version
# xz -9e junit-%version.tar
Source0:	junit-%{version}.tar.xz
Patch0:		http://patch-tracker.debian.org/patch/series/dl/junit4/4.10-3/java7-ignore-test.patch
BuildArch:	noarch
BuildRequires:	ant
BuildRequires:	hamcrest
BuildRequires:	jpackage-utils >= 0:1.7.4
BuildRequires:	java-1.7.0-devel
Requires(post,postun):	jpackage-utils >= 0:1.7.4
Requires:		java-1.6.0
Requires:		hamcrest
%rename junit4

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck. 
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and 
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
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%package demo
Group:		Development/Java
Summary:	Demos for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
%patch0 -p1 -b .ignoretest~
find . -type f -name "*.jar" | xargs -t rm
ln -s $(build-classpath hamcrest/core) lib/hamcrest-core-1.1.jar
perl -pi -e 's/\r$//g' stylesheet.css

%build
export CLASSPATH=
export OPT_JAR_LIST=:
export JAVA_HOME=%{_jvm/java-1.7.0
ant -Dant.build.javac.source=1.5 dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 junit%{version}/junit-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir} 
ln -sf %{name}-%{version}.jar %{name}.jar
popd

# pom
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
sed -e "s,@artifactId@,%name,g;s,@version@,%version,g" build/maven/pom-template.xml >%{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap junit junit %{version} JPP %{name}

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr junit%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/demo/junit # Not using %%name for last part because it is 
                                                                # part of package name
cp -pr junit%{version}/junit/* %{buildroot}%{_datadir}/%{name}/demo/junit

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc cpl-v10.html README.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*

%files demo
%{_datadir}/%{name}

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%doc junit%{version}/doc/*

