%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

Name:           jgettext
Version:        0.12
Release:        1%{?dist}
Summary:        An ANTLR-based parser and generator for GNU Gettext PO/POT 

Group:          Development/Libraries
License:        LGPLv2
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
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  antlr
BuildRequires:  antlr-maven-plugin
BuildRequires:  junit
BuildRequires:  gettext

Requires:       jpackage-utils
Requires:       java

%description
JGettext includes an ANTLR-based parser for GNU Gettext PO/POT files and a 
PO/POT generator as well.

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
cp -p target/jgettext*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

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
* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 0.12-1
- Version 0.12

* Mon Feb 4 2013 Patrick Huang <pahuang@redhat.com> 0.11-1
- Initial RPM package
