%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

Name:           openprops
Version:        0.6
Release:        3%{?dist}
Summary:        A fork of java.util.Properties from OpenJDK

Group:          Development/Libraries
License:        GPLv2 with exceptions
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{name}-%{version}.zip

BuildArch:      noarch

BuildRequires:  jpackage-utils

BuildRequires:  java-devel

BuildRequires:  %mvnbuildRequires

BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  junit

Requires:       jpackage-utils
Requires:       java

%description
OpenProps is a tiny Java library which reads and writes .properties files 
using the same code as java.util.Properties from the OpenJDK, but enhanced so
that it preserves the order of entries within the file, and it also preserves
comments in the file.  
This means that a Properties editor or a file converter written to use 
OpenProps won't have to lose comments or mess up the order of entries. 

By using OpenJDK code, OpenProps should handle all the old corner-cases in 
exactly the same way Java does.  The handling of whitespace and comments is
tested by a number of JUnit tests.  But please let me know if you find a bug!

Note the following differences from java.util.Properties:

1. preserves comments and the order of entries in the file
2. storeToXml doesn't use the Sun DTD (or any DTD) because it adds attributes 
   for comments.
3. equals() and hashCode() won't work the same way as with java.util.Properties,
   because they are no longer inherited from Hashtable.  
   All you get is identity equality/hashcode.

Also note that any header comment in the .properties file will be interpreted as
a comment attached to the first message.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version} 
 
%build
mvn-rpmbuild package javadoc:aggregate

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%doc README.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 0.6-3
- Update BuildRequires maven/maven-local depend on dist version

* Wed Feb 6 2013 Patrick Huang <pahuang@redhat.com> 0.6-2
- Update BuildRequires to make it work in f18 and f19

* Fri Feb 1 2013 Patrick Huang <pahuang@redhat.com> 0.6-1
- Initial RPM package
