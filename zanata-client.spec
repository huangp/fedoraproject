%if 0%{?fedora} > 18
    %global mvn_exec_plugin exec-maven-plugin
%else
    %global mvn_exec_plugin maven-plugin-exec
%endif

%global shortname client

%global submodule_rest zanata-rest-%{shortname}
%global submodule_commands zanata-%{shortname}-commands
%global submodule_cli zanata-cli

Name:           zanata-%{shortname}
Version:        2.0.1
Release:        1%{?dist}
Summary:        Zanata API modules

Group:          Development/Tools
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
Requires:       slf4j 

# dependencies in zanata-rest-client
Requires:       zanata-api
BuildRequires:  junit
Requires:       resteasy

# dependencies in zanata-common-commands
Requires:       zanata-common
BuildRequires:  mockito
Requires:       apache-commons-configuration
Requires:       log4j
Requires:       args4j
Requires:       openprops
Requires:       apache-commons-collections
Requires:       guava
BuildRequires:  hamcrest12
Requires:       apache-commons-lang
Requires:       apache-commons-codec
Requires:       apache-commons-io
Requires:       opencsv
Requires:       ant

# dependencies in zanata-cli
BuildRequires:  %mvn_exec_plugin

Requires:       jpackage-utils
Requires:       java
BuildRequires:	help2man


%description
Zanata common modules

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{shortname}.
This includes submodules:
%{submodule_rest}, %{submodule_commands} and %{submodule_cli}.

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

# local offline maven can not resolve each module, 
# we have to disable our own module and generate classpath one by one
cd %{submodule_rest}
mvn-rpmbuild dependency:build-classpath -DincludeScope=compile -Dmdep.outputFile=target/%{submodule_rest}-classpath.txt

cd ..
%pom_remove_dep org.zanata:%{submodule_rest} %{submodule_commands}
cd %{submodule_commands}
mvn-rpmbuild dependency:build-classpath -DincludeScope=compile -Dmdep.outputFile=target/%{submodule_commands}-classpath.txt

cd ..
%pom_remove_dep org.zanata:%{submodule_commands} %{submodule_cli}
cd %{submodule_cli}
mvn-rpmbuild dependency:build-classpath -DincludeScope=compile -Dmdep.outputFile=target/%{submodule_cli}-classpath.txt


%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}

%global ver SNAPSHOT
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

rest_cp=$(cat %{submodule_rest}/target/%{submodule_rest}-classpath.txt)
commands_cp=$(cat %{submodule_commands}/target/%{submodule_commands}-classpath.txt)
cli_cp=$(cat %{submodule_cli}/target/%{submodule_cli}-classpath.txt)

%global CLASSPATH $rest_cp:$commands_cp:$cli_cp

mkdir -p $RPM_BUILD_ROOT%{_bindir}

install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
# create wrapper script
# adapted from jpackage_script(). 
# We build CLASSPATH at build time and the script won't be able to access it at runtime
############# copied from jpackage_script() ###########################
cat > $RPM_BUILD_ROOT%{_bindir}/zanata-cli << ZANATA_CLI
#!/bin/sh
#
# %{name} script
# JPackage Project <http://www.jpackage.org/>

# Source functions library
. %{_javadir}-utils/java-functions

# Source system prefs
if [ -f %{_sysconfdir}/java/%{name}.conf ] ; then
  . %{_sysconfdir}/java/%{name}.conf
fi

# Source user prefs
if [ -f \$HOME/.%{name}rc ] ; then
  . \$HOME/.%{name}rc
fi

# Configuration
MAIN_CLASS=org.zanata.client.ZanataClient
BASE_JARS="%{submodule_rest} %{submodule_commands} %{submodule_cli} slf4j/log4j12"
CLASSPATH=%{CLASSPATH}

# Set parameters
set_jvm
# we have built CLASSPATH above
set_classpath \$BASE_JARS

# Let's start
run "\$@"
ZANATA_CLI

chmod 755 $RPM_BUILD_ROOT%{_bindir}/zanata-cli
#################################################################

# man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
help2man $RPM_BUILD_ROOT%{_bindir}/zanata-cli > %{buildroot}%{_mandir}/man1/zanata-cli.1

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{submodule_rest}.pom
%{_mavenpomdir}/JPP-%{submodule_commands}.pom
%{_mavenpomdir}/JPP-%{submodule_cli}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{submodule_rest}.jar
%{_javadir}/%{submodule_commands}.jar
%{_javadir}/%{submodule_cli}.jar
%attr(0755,root,root) %{_bindir}/zanata-cli
%attr(0644,root,root) %doc %_mandir/man1/zanata-cli.1.gz

%files javadoc
%{_javadocdir}/%{submodule_rest}
%{_javadocdir}/%{submodule_commands}
%{_javadocdir}/%{submodule_cli}

%changelog
* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.0.1-1
- Initial RPM package
