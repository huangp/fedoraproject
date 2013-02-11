%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

%define shortname common
%define submodule_util zanata-%{shortname}-util

Name:           zanata-%{shortname}
Version:        2.1.1
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
BuildRequires:  zanata-api
BuildRequires:  jackson
BuildRequires:  guava
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-codec
BuildRequires:  hamcrest12
BuildRequires:  slf4j 
BuildRequires:  junit     
BuildRequires:  testng           

Requires:       jpackage-utils
Requires:       java

%description
Zanata common modules

%package javadoc
Summary:        Javadocs for %{submodule_util}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{shortname}.



%prep
%setup -q -n %{name}-%{shortname}-%{version}
# Disables child-module-1, a submodule of the main pom.xml file
%pom_disable_module zanata-adapter-po
%pom_disable_module zanata-adapter-properties
%pom_disable_module zanata-adapter-xliff
%pom_disable_module zanata-adapter-glossary



# we need to tweek some dependencies for it to build in fedora
# Removes dependency
#%pom_remove_dep groupId:artifactId
# Adds new dependency
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>blah</groupId><artifactId>blah</artifactId><version>1</version></dependency>"
#%pom_remove_plugin :maven-dependency-plugin

%build

# -Dmaven.local.debug=true
mvn-rpmbuild package javadoc:aggregate 

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}

cp -p %{submodule_util}/target/%{submodule_util}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_util}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_util}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{submodule_util}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_util}.pom

%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{submodule_util}.pom %{submodule_util}.jar

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{submodule_util}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{submodule_util}.jar
%doc

%files javadoc
%{_javadocdir}/%{submodule_util}

%changelog
* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.1.1-1
- Initial RPM package
