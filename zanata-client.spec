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
Version:        2.2.0
Release:        1%{?dist}
Summary:        Zanata API modules

Group:          Development/Tools
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

BuildArch:      noarch

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
BuildRequires:  hamcrest
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-io
BuildRequires:  opencsv
BuildRequires:  ant

# dependencies in zanata-cli
BuildRequires:  %mvn_exec_plugin

Requires:       jpackage-utils
Requires:       java
#BuildRequires:	help2man

Requires:       slf4j
Requires:       zanata-api
Requires:       resteasy
Requires:       zanata-common
Requires:       apache-commons-configuration
Requires:       log4j
Requires:       args4j
Requires:       openprops
Requires:       apache-commons-collections
Requires:       guava
Requires:       apache-commons-lang
Requires:       apache-commons-codec
Requires:       apache-commons-io
Requires:       opencsv
Requires:       ant


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
%setup -q -n %{name}-%{shortname}-%{version}
#%setup -q -n %{name}-master
%pom_disable_module zanata-maven-plugin 
%pom_remove_plugin :appassembler-maven-plugin %{submodule_cli}
%pom_remove_plugin :maven-assembly-plugin %{submodule_cli}

%build

# -Dmaven.local.debug=true
%mvn_build -- -Dmdep.analyze.skip=true

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

%mvn_install

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
BASE_JARS="%{submodule_rest} %{submodule_commands} %{submodule_cli} slf4j/log4j12 opencsv"
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
#mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
#help2man $RPM_BUILD_ROOT%{_bindir}/zanata-cli > %{buildroot}%{_mandir}/man1/zanata-cli.1

#%check
#mvn-rpmbuild verify

%files -f .mfiles
%attr(0755,root,root) %{_bindir}/zanata-cli
#%attr(0644,root,root) %doc %_mandir/man1/zanata-cli.1.gz
%doc README.txt

%files javadoc -f .mfiles-javadoc

%changelog
* Fri Mar 1 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream version update

* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.0.1-1
- Initial RPM package
