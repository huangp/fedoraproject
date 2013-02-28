%global shortname api
%global submodule zanata-common-%{shortname}

Name:           zanata-%{shortname}
Version:        2.2.0
Release:        1%{?dist}
Summary:        Zanata API modules

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

BuildArch:      noarch

BuildRequires:  jpackage-utils

BuildRequires:  java-devel

BuildRequires:  maven-local

BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:  hamcrest12
BuildRequires:  testng

# required lib at compile time
BuildRequires:  hibernate-validator
BuildRequires:  jackson
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-codec
BuildRequires:  resteasy
BuildRequires:  slf4j
BuildRequires:  jboss-annotations-1.1-api

# runtime dependencies
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
#cd zanata-common-api/src/test/java/
#find . -type f -name "*Test.java" | xargs rm 

%build

# -Dmaven.local.debug=true
mvn-rpmbuild package javadoc:aggregate -Dmaven.test.skip=true

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p %{submodule}/target/%{submodule}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{submodule}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule}.pom

%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{submodule}.pom %{submodule}.jar

#%check
#mvn-rpmbuild verify

%files -f .mfiles
%doc README.txt

%files javadoc
%{_javadocdir}/%{submodule}

%changelog
* Wed Feb 27 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream update to version 2.2.0

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 2.1.0-1
- Initial RPM package
