%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

%define shortname common

%define submodule_util zanata-%{shortname}-util
%define submodule_po zanata-adapter-po
%define submodule_properties zanata-adapter-properties
%define submodule_xliff zanata-adapter-xliff
%define submodule_glossary zanata-adapter-glossary

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
BuildRequires:  hamcrest12
BuildRequires:  slf4j 
BuildRequires:  testng 

# dependencies in zanata-common-util
BuildRequires:  jackson
BuildRequires:  guava
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-codec
BuildRequires:  junit     

# dependencies in zanata-adapter-po
BuildRequires:  jgettext
BuildRequires:  apache-commons-lang

# dependencies in zanata-adapter-properties
BuildRequires:  openprops

# dependencies in zanata-adapter-xliff (no extra)

# dependencies in zanata-adapter-glossary
BuildRequires:  opencsv

Requires:       jpackage-utils
Requires:       java

%description
Zanata common modules

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{shortname}.
This includes submodules:
%{submodule_util}, %{submodule_po}, %{submodule_properties}, %{submodule_xliff} 
and %{submodule_glossary}

%prep
# TODO change back to version
#%setup -q -n %{name}-%{shortname}-%{version}
%setup -q -n %{name}-master
# Disables child-module-1, a submodule of the main pom.xml file
# Removes dependency
# %pom_remove_dep org.infinitest:infinitest %{submodule_properties}



# we need to tweek some dependencies for it to build in fedora
# Removes dependency
#%pom_remove_dep groupId:artifactId
# Adds new dependency
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>blah</groupId><artifactId>blah</artifactId><version>1</version></dependency>"
%pom_remove_plugin :maven-dependency-plugin

%build

# -Dmaven.local.debug=true
mvn-rpmbuild package javadoc:aggregate 

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}

%define ver SNAPSHOT
# TODO change *-SNAPSHOT to %{version}
cp -p %{submodule_util}/target/%{submodule_util}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_util}.jar
cp -p %{submodule_po}/target/%{submodule_po}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_po}.jar
cp -p %{submodule_properties}/target/%{submodule_properties}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_properties}.jar
cp -p %{submodule_xliff}/target/%{submodule_xliff}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_xliff}.jar
cp -p %{submodule_glossary}/target/%{submodule_glossary}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_glossary}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_util}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_po}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_properties}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_xliff}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_glossary}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{submodule_util}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_util}.pom
install -pm 644 %{submodule_po}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_po}.pom
install -pm 644 %{submodule_properties}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_properties}.pom
install -pm 644 %{submodule_xliff}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_xliff}.pom
install -pm 644 %{submodule_glossary}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_glossary}.pom

%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{submodule_util}.pom %{submodule_util}.jar
%add_maven_depmap JPP-%{submodule_po}.pom %{submodule_po}.jar
%add_maven_depmap JPP-%{submodule_properties}.pom %{submodule_properties}.jar
%add_maven_depmap JPP-%{submodule_xliff}.pom %{submodule_xliff}.jar
%add_maven_depmap JPP-%{submodule_glossary}.pom %{submodule_glossary}.jar

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{submodule_util}.pom
%{_mavenpomdir}/JPP-%{submodule_po}.pom
%{_mavenpomdir}/JPP-%{submodule_properties}.pom
%{_mavenpomdir}/JPP-%{submodule_xliff}.pom
%{_mavenpomdir}/JPP-%{submodule_glossary}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{submodule_util}.jar
%{_javadir}/%{submodule_po}.jar
%{_javadir}/%{submodule_properties}.jar
%{_javadir}/%{submodule_xliff}.jar
%{_javadir}/%{submodule_glossary}.jar
%doc

%files javadoc
%{_javadocdir}/%{submodule_util}
%{_javadocdir}/%{submodule_po}
%{_javadocdir}/%{submodule_properties}
%{_javadocdir}/%{submodule_xliff}
%{_javadocdir}/%{submodule_glossary}

%changelog
* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.1.1-1
- Initial RPM package
