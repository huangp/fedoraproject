%global shortname common

%global submodule_util zanata-%{shortname}-util
%global submodule_po zanata-adapter-po
%global submodule_properties zanata-adapter-properties
%global submodule_xliff zanata-adapter-xliff
%global submodule_glossary zanata-adapter-glossary

Name:           zanata-%{shortname}
Version:        2.2.1
Release:        1%{?dist}
Summary:        Zanata API modules

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

BuildArch:      noarch

BuildRequires:	maven-local 

BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:	zanata-api
BuildRequires:	slf4j
BuildRequires:  testng
BuildRequires:  hamcrest12

# dependencies in zanata-common-util
BuildRequires:	jackson
BuildRequires:	guava
BuildRequires:	apache-commons-io
BuildRequires:	apache-commons-codec
BuildRequires:  junit

# dependencies in zanata-adapter-pvo
BuildRequires:	jgettext
BuildRequires:	apache-commons-lang

# dependencies in zanata-adapter-properties
BuildRequires:	openprops

# dependencies in zanata-adapter-xliff (no extra)

# dependencies in zanata-adapter-glossary
BuildRequires:	opencsv

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

%description javadoc
This package contains the API documentation for %{shortname}.
This includes submodules:
%{submodule_util}, %{submodule_po}, %{submodule_properties}, %{submodule_xliff} 
and %{submodule_glossary}

%prep
%setup -q -n %{name}-%{shortname}-%{version}
#%setup -q -n %{name}-master
%pom_remove_plugin :maven-dependency-plugin

%build

# -Dmaven.local.debug=true
%if 0%{?fedora} > 18
%mvn_build --skip-tests
%else
mvn-rpmbuild package javadoc:aggregate -Dmaven.test.skip=true
%endif

%install

%if 0%{?fedora} > 18
%mvn_install
%else
mkdir -p $RPM_BUILD_ROOT%{_javadir}

cp -p %{submodule_util}/target/%{submodule_util}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_util}.jar
cp -p %{submodule_po}/target/%{submodule_po}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_po}.jar
cp -p %{submodule_properties}/target/%{submodule_properties}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_properties}.jar
cp -p %{submodule_xliff}/target/%{submodule_xliff}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_xliff}.jar
cp -p %{submodule_glossary}/target/%{submodule_glossary}*-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{submodule_glossary}.jar

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
%endif

%files -f .mfiles
%doc README.txt COPYING.LESSER COPYING.GPL

%if 0%{?fedora} > 18
%files javadoc -f .mfiles-javadoc
%else
%files javadoc
%{_javadocdir}/%{submodule_util}
%{_javadocdir}/%{submodule_po}
%{_javadocdir}/%{submodule_properties}
%{_javadocdir}/%{submodule_xliff}
%{_javadocdir}/%{submodule_glossary}
%endif

%changelog
* Tue Mar 19 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-1
- Upstream version update

* Thu Feb 28 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream version update

* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.1.1-1
- Initial RPM package
