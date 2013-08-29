%global shortname client

%global submodule_rest zanata-rest-%{shortname}
%global submodule_commands zanata-%{shortname}-commands
%global submodule_cli zanata-cli

Name:           zanata-%{shortname}
Version:        3.1.1
Release:        1%{?dist}
Summary:        Zanata client module

Group:          Development/Tools
License:        LGPLv2+
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip
Patch0:         slf4j-backward-compatible-fix.patch

BuildArch:      noarch

BuildRequires:  maven-local

BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-testng
BuildRequires:  maven-surefire-provider-junit4

# dependencies in zanata-rest-client
BuildRequires:  zanata-parent
BuildRequires:  zanata-api
BuildRequires:  junit
BuildRequires:  resteasy
%if 0%{?fedora} < 19
BuildRequires:  apache-james-project
%endif

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
BuildRequires:  exec-maven-plugin 
BuildRequires:  powermock-junit4
BuildRequires:  powermock-api-mockito
BuildRequires:  powermock-core

Requires:       jpackage-utils
Requires:       java

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
Zanata client modules. 
Holds most of Zanata's client code, including Zanata CLI.
It also contains REST stub for interacting with a Zanata server.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils
Requires:       %{name} = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{shortname}.
This includes submodules:
%{submodule_rest}, %{submodule_commands} and %{submodule_cli}.

%prep
%setup -q -n %{name}-%{shortname}-%{version}
%pom_disable_module zanata-maven-plugin 
%pom_remove_plugin :appassembler-maven-plugin %{submodule_cli}
%pom_remove_plugin :maven-assembly-plugin %{submodule_cli}

%build
# -Dmaven.local.debug=true
%mvn_build -- -Dmdep.analyze.skip=true -e

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

mkdir -p %{buildroot}%{_bindir}

install -d -m 755 %{buildroot}%{_bindir}
# create wrapper script
# adapted from jpackage_script(). 
# We build CLASSPATH at build time and the script won't be able to access it at runtime
############# copied from jpackage_script() ###########################
cat > %{buildroot}%{_bindir}/zanata-cli << ZANATA_CLI
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

chmod 755 %{buildroot}%{_bindir}/zanata-cli
#################################################################


%files -f .mfiles
%dir %{_javadir}/%{name}
%attr(0755,root,root) %{_bindir}/zanata-cli
%doc README.txt

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Aug 28 2013 Patrick Huang <pahuang@redhat.com> 3.1.1-1
- Upstream update for newer version of RESTEasy

* Wed Aug 28 2013 Patrick Huang <pahuang@redhat.com> 3.1.0-1
- Upstream update

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-2
- Change license to LGPLv2+

* Fri Mar 1 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream version update

* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.0.1-1
- Initial RPM package
