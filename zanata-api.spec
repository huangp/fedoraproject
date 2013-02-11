%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

%define shortname api
%define submodule zanata-common-%{shortname}

Name:           zanata-%{shortname}
Version:        2.1.0
Release:        1%{?dist}
Summary:        Zanata API modules

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

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
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:  hibernate-validator
BuildRequires:  jackson
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-codec
BuildRequires:  hamcrest12
BuildRequires:  testng
BuildRequires:  resteasy
BuildRequires:  slf4j
BuildRequires:  jboss-annotations-1.1-api

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
# TODO change back to version
#%setup -q -n %{name}-%{shortname}-%{version}
%setup -q -n %{name}-integration-master
# we need to tweek some dependencies for it to build in fedora
# Removes dependency
#%pom_remove_dep groupId:artifactId
# Adds new dependency
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>blah</groupId><artifactId>blah</artifactId><version>1</version></dependency>"
%pom_remove_plugin :maven-dependency-plugin %{submodule}

%build

# -Dmaven.local.debug=true
mvn-rpmbuild package javadoc:aggregate 

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
# TODO change *-SNAPSHOT to %{version}
cp -p %{submodule}/target/%{submodule}*-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{submodule}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule}.pom

%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{submodule}.pom %{submodule}.jar

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{submodule}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{submodule}.jar
%doc

%files javadoc
%{_javadocdir}/%{submodule}

%changelog
* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 2.1.0-1
- Initial RPM package
