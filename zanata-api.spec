%global shortname api
%global submodule zanata-common-%{shortname}

Name:           zanata-%{shortname}
Version:        2.2.0
Release:        1%{?dist}
Summary:        Zanata API modules

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip
#Source3:        hamcrest-depmap.xml
#Patch0:         0001-fix-static-import-for-openJDK-7.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils

BuildRequires:  maven-local
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:  hamcrest12
BuildRequires:  testng

# dependencies in zanata-common-api
BuildRequires:  hibernate-validator
Requires:       hibernate-validator
BuildRequires:  jackson
Requires:       jackson
BuildRequires:  apache-commons-lang
Requires:       apache-commons-lang
BuildRequires:  apache-commons-codec
Requires:       apache-commons-codec
BuildRequires:  resteasy
Requires:       resteasy
BuildRequires:  slf4j
Requires:       slf4j
BuildRequires:  jboss-annotations-1.1-api
Requires:       jboss-annotations-1.1-api

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
%setup -q -n %{name}-%{shortname}-%{version}
%pom_remove_plugin :maven-dependency-plugin %{submodule}
#%patch0

# see below todo tag
#%pom_remove_dep org.hamcrest:hamcrest-core %{submodule}
#%pom_remove_dep org.hamcrest:hamcrest-library %{submodule}
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>org.hamcrest</groupId><artifactId>hamcrest-core</artifactId><version>1.2</version><scope>test</scope></dependency>" %{submodule}
#%pom_xpath_inject "pom:dependencies" "<dependency><groupId>org.hamcrest</groupId><artifactId>hamcrest-library</artifactId><version>1.2</version><scope>test</scope></dependency>" %{submodule}

%build

# -Dmaven.local.debug=true
# TODO we want to use hamcrest12 but it has a bug rhbz#917857 in fedora we can not compile test classes in rawhide
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
%doc README.txt 

%if 0%{?fedora} > 18
%files javadoc -f .mfiles-javadoc
%else
%files javadoc
%{_javadocdir}/%{submodule}
%endif

%changelog
* Wed Feb 27 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream update to version 2.2.0

* Thu Feb 7 2013 Patrick Huang <pahuang@redhat.com> 2.1.0-1
- Initial RPM package
