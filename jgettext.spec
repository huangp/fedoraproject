Name:           jgettext
Version:        0.13
Release:        1%{?dist}
Summary:        An ANTLR-based parser and generator for GNU Gettext PO/POT 

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{name}-%{version}.zip

BuildArch:      noarch

BuildRequires:  jpackage-utils

BuildRequires:  java-devel

BuildRequires:  maven-local

BuildRequires:  maven-install-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-junit4
Requires:       antlr
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
%if 0%{?fedora} >= 19
%mvn_build
%else
mvn-rpmbuild package javadoc:aggregate
%endif


%install
%if 0%{?fedora} >= 19
%mvn_install
%else
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/jgettext*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap
%endif

%files -f .mfiles
%doc README.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Tue Mar 19 2013 Patrick Huang <pahuang@redhat.com> 0.13-1
- Upstream version upgrade and fix issue in review process

* Tue Feb 19 2013 Patrick Huang <pahuang@redhat.com> 0.12-2
- Update maven-local and file section using new macro

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 0.12-1
- Version 0.12

* Mon Feb 4 2013 Patrick Huang <pahuang@redhat.com> 0.11-1
- Initial RPM package
