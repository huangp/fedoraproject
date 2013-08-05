%global shortname common

%global submodule_util zanata-%{shortname}-util
%global submodule_po zanata-adapter-po
%global submodule_properties zanata-adapter-properties
%global submodule_xliff zanata-adapter-xliff
%global submodule_glossary zanata-adapter-glossary

Name:           zanata-%{shortname}
Version:        2.2.1
Release:        5%{?dist}
Summary:        Zanata common modules

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

BuildArch:      noarch

BuildRequires:  maven-local 

BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:  zanata-parent
BuildRequires:  zanata-api
%if 0%{?fedora} < 19
BuildRequires:  apache-james-project
%endif
BuildRequires:  slf4j
BuildRequires:  testng
BuildRequires:  hamcrest

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
Requires:       zanata-api
Requires:       slf4j

Requires:       jackson
Requires:       guava
Requires:       apache-commons-io
Requires:       apache-commons-codec

Requires:       jgettext
Requires:       apache-commons-lang

Requires:       openprops

Requires:       opencsv

%description
Zanata common modules


%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils
Requires:       %{name} = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{shortname}.
This includes submodules:
%{submodule_util}, 
%{submodule_po}, 
%{submodule_properties}, 
%{submodule_xliff} and %{submodule_glossary}

%prep
%setup -q -n %{name}-%{shortname}-%{version}
%pom_remove_plugin :maven-dependency-plugin

%build
%if 0%{?fedora} > 19
%mvn_build
%endif
%if 0%{?fedora} == 19
%mvn_build --skip-tests
%else
mvn-rpmbuild package javadoc:aggregate -Dmaven.test.skip=true
%endif

%install
%if 0%{?fedora} > 18
%mvn_install
%else
mkdir -p %{buildroot}%{_javadir}

cp -p %{submodule_util}/target/%{submodule_util}*-%{version}.jar %{buildroot}%{_javadir}/%{submodule_util}.jar
cp -p %{submodule_po}/target/%{submodule_po}*-%{version}.jar %{buildroot}%{_javadir}/%{submodule_po}.jar
cp -p %{submodule_properties}/target/%{submodule_properties}*-%{version}.jar %{buildroot}%{_javadir}/%{submodule_properties}.jar
cp -p %{submodule_xliff}/target/%{submodule_xliff}*-%{version}.jar %{buildroot}%{_javadir}/%{submodule_xliff}.jar
cp -p %{submodule_glossary}/target/%{submodule_glossary}*-%{version}.jar %{buildroot}%{_javadir}/%{submodule_glossary}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{submodule_util}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{submodule_po}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{submodule_properties}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{submodule_xliff}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{submodule_glossary}

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
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
%endif



%files -f .mfiles
%if 0%{?fedora} > 18
%dir %{_javadir}/%{name}
%endif
%doc README.txt COPYING.LESSER COPYING.GPL

%if 0%{?fedora} > 18
%files javadoc -f .mfiles-javadoc
%else
%files javadoc
%{_javadocdir}/%{name}/%{submodule_util}
%{_javadocdir}/%{name}/%{submodule_po}
%{_javadocdir}/%{name}/%{submodule_properties}
%{_javadocdir}/%{name}/%{submodule_xliff}
%{_javadocdir}/%{name}/%{submodule_glossary}
%endif


%changelog
* Fri May 3 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-5
- Minor cosmetic change

* Fri May 3 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-4
- Minor cosmetic change

* Fri May 3 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-3
- Remove javadoc subpackage require %{?_isa}
- Change javadoc installation location
- Change license to LGPLv2+

* Wed May 1 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-2
- Add missing pom for f19-

* Tue Mar 19 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-1
- Upstream version update

* Thu Feb 28 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream version update

* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.1.1-1
- Initial RPM package
