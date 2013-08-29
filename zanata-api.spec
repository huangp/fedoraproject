%global shortname api
%global submodule zanata-common-%{shortname}

Name:           zanata-%{shortname}
Version:        3.0.1
Release:        1%{?dist}
Summary:        Zanata API modules

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
BuildRequires:  hamcrest
BuildRequires:  testng

# dependencies in zanata-common-api
BuildRequires:  hibernate-validator
BuildRequires:  jackson
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-codec
BuildRequires:  resteasy
%if 0%{?fedora} < 19
BuildRequires:  apache-james-project
%endif
BuildRequires:  slf4j
BuildRequires:  jboss-annotations-1.1-api


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
Requires:       %{name} = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{submodule}.



%prep
%setup -q -n %{name}-%{shortname}-%{version}
%pom_remove_plugin :maven-dependency-plugin %{submodule}
%pom_remove_plugin :gmaven-plugin %{submodule}
%pom_remove_plugin :maven-shade-plugin %{submodule}

%build

# -Dmaven.local.debug=true
#%mvn_build --skip-tests
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
%endif

%files -f .mfiles
%if 0%{?fedora} > 18
%dir %{_javadir}/%{name}
%endif
%doc README.txt 

%if 0%{?fedora} > 18
%files javadoc -f .mfiles-javadoc
%else
%files javadoc
%{_javadocdir}/%{submodule}
%endif

%changelog
* Thu Aug 22 2013 Patrick Huang <pahuang@redhat.com> 3.0.1-1
- Latest upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 3 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-7
- Remove javadoc subpackage require %{?_isa}

* Tue Apr 23 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-6
- Change license to LGPLv2+ and add subpackage requires according to review

* Tue Apr 23 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-5
- Add BR apache-james-project for f19-

* Mon Apr 22 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-4
- Disable test in f19 due to hamcrest compatibility bug

* Mon Apr 22 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-3
- Add conditional build for f19-

* Wed Apr 17 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-2
- Remove conditional build

* Wed Feb 27 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream update to version 2.2.0

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 2.1.0-1
- Initial RPM package
