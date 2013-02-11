%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
    %define mvn_exec_plugin exec-maven-plugin
%else
    %define mvnbuildRequires maven
    %define mvn_exec_plugin maven-plugin-exec
%endif

%define shortname client

%define submodule_rest zanata-rest-%{shortname}
%define submodule_commands zanata-%{shortname}-commands
%define submodule_cli zanata-cli

Name:           zanata-%{shortname}
Version:        2.0.1
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
BuildRequires:  slf4j 

# dependencies in zanata-rest-client
BuildRequires:  zanata-api
BuildRequires:  junit
BuildRequires:  resteasy

# dependencies in zanata-common-commands
BuildRequires:  zanata-common
BuildRequires:  mockito
BuildRequires:  apache-commons-configuration
BuildRequires:  log4j
BuildRequires:  args4j
BuildRequires:  openprops
BuildRequires:  apache-commons-collections
BuildRequires:  guava
BuildRequires:  hamcrest12
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-io
BuildRequires:  opencsv
BuildRequires:  ant

# dependencies in zanata-cli
BuildRequires:  %mvn_exec_plugin

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
%{submodule_rest}, %{submodule_commands}

%prep
# TODO change back to version
#%setup -q -n %{name}-%{shortname}-%{version}
%setup -q -n %{name}-master
# Disables child-module-1, a submodule of the main pom.xml file
# Removes dependency
%pom_disable_module zanata-maven-plugin



# we need to tweek some dependencies for it to build in fedora
# Removes dependency
#%pom_remove_dep groupId:artifactId
# Adds new dependency
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>blah</groupId><artifactId>blah</artifactId><version>1</version></dependency>"
%pom_remove_plugin :appassembler-maven-plugin %{submodule_cli}
%pom_remove_plugin :maven-assembly-plugin %{submodule_cli}

%build

# -Dmaven.local.debug=true
mvn-rpmbuild package javadoc:aggregate

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}

%define ver SNAPSHOT
# TODO change *-SNAPSHOT to %{version}
cp -p %{submodule_rest}/target/%{submodule_rest}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_rest}.jar
cp -p %{submodule_commands}/target/%{submodule_commands}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_commands}.jar
cp -p %{submodule_cli}/target/%{submodule_cli}*-%{ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_cli}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_rest}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_commands}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{submodule_cli}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{submodule_rest}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_rest}.pom
install -pm 644 %{submodule_commands}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_commands}.pom
install -pm 644 %{submodule_cli}/pom.xml  %{buildroot}%{_mavenpomdir}/JPP-%{submodule_cli}.pom

%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{submodule_rest}.pom %{submodule_rest}.jar
%add_maven_depmap JPP-%{submodule_commands}.pom %{submodule_commands}.jar
%add_maven_depmap JPP-%{submodule_cli}.pom %{submodule_cli}.jar

%check
mvn-rpmbuild verify -DignoreNonCompile

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{submodule_rest}.pom
%{_mavenpomdir}/JPP-%{submodule_commands}.pom
%{_mavenpomdir}/JPP-%{submodule_cli}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{submodule_rest}.jar
%{_javadir}/%{submodule_commands}.jar
%{_javadir}/%{submodule_cli}.jar
%doc

%files javadoc
%{_javadocdir}/%{submodule_rest}
%{_javadocdir}/%{submodule_commands}
%{_javadocdir}/%{submodule_cli}

%changelog
* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.0.1-1
- Initial RPM package
