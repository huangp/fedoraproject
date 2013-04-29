Name:           openprops
Version:        0.6
Release:        5%{?dist}
Summary:        An improved java.util.Properties from OpenJDK

Group:          Development/Libraries
License:        GPLv2 with exceptions
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{name}-%{version}.zip

BuildArch:      noarch

BuildRequires:  maven-local

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
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc README.txt COPYING.txt

%files -f .mfiles-javadoc
%doc COPYING.txt


%changelog
* Mon Apr 29 2013 Patrick Huang <pahuang@redhat.com> 0.6-5
- Adapt latest java packacking guideline

* Tue Feb 19 2013 Patrcik Huang <pahuang@redhat.com> 0.6-4
- Add COPYING.txt into package and update summary and simplify file section

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 0.6-3
- Update BuildRequires maven/maven-local depend on dist version

* Wed Feb 6 2013 Patrick Huang <pahuang@redhat.com> 0.6-2
- Update BuildRequires to make it work in f18 and f19

* Fri Feb 1 2013 Patrick Huang <pahuang@redhat.com> 0.6-1
- Initial RPM package
