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
#Source3:        hamcrest-depmap.xml
#Patch0:         0001-fix-static-import-for-openJDK-7.patch

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
#%patch0

# see below todo tag
#%pom_remove_dep org.hamcrest:hamcrest-core %{submodule}
#%pom_remove_dep org.hamcrest:hamcrest-library %{submodule}
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>org.hamcrest</groupId><artifactId>hamcrest-core</artifactId><version>1.2</version><scope>test</scope></dependency>" %{submodule}
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>org.hamcrest</groupId><artifactId>hamcrest-library</artifactId><version>1.2</version><scope>test</scope></dependency>" %{submodule}

%build

# -Dmaven.local.debug=true
# TODO we want to use hamcrest12 but it has a bug rhbz#917857 in fedora we can not compile test classes in rawhide
#%mvn_build --skip-tests
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.txt 

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Apr 17 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-2
- Remove conditional build and only target f19

* Wed Feb 27 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream update to version 2.2.0

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 2.1.0-1
- Initial RPM package
