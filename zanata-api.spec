%global shortname api
%global submodule zanata-common-%{shortname}

Name:           zanata-%{shortname}
Version:        2.2.0
Release:        2%{?dist}
Summary:        Zanata API modules

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:  zanata-parent
BuildRequires:  hamcrest
BuildRequires:  testng

# dependencies in zanata-common-api
BuildRequires:  hibernate-validator
BuildRequires:  jackson
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-codec
BuildRequires:  resteasy
BuildRequires:  slf4j
BuildRequires:  jboss-annotations-1.1-api


Requires:       hibernate-validator
Requires:       jackson
Requires:       apache-commons-lang
Requires:       apache-commons-codec
Requires:       resteasy
Requires:       slf4j
Requires:       jboss-annotations-1.1-api

Requires:       jpackage-utils
Requires:       java

%description
Zanata API modules

%package javadoc
Summary:        Javadocs for %{submodule}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{submodule}.



%prep
%setup -q -n %{name}-%{shortname}-%{version}
%pom_remove_plugin :maven-dependency-plugin %{submodule}

%build

# -Dmaven.local.debug=true
#%mvn_build --skip-tests
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.txt 

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Apr 17 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-2
- Remove conditional build

* Wed Feb 27 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream update to version 2.2.0

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 2.1.0-1
- Initial RPM package
