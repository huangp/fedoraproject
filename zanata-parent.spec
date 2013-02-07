%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

%define shortname parent

Name:           zanata-%{shortname}
Version:        9
Release:        1%{?dist}
Summary:        The Project Object Model(pom) files for the Zanata packages.

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{name}-%{version}.zip

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
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4

Requires:       jpackage-utils
Requires:       java

%description
The Project Object Model(pom) files for the Zanata packages.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build

mvn-rpmbuild install

%install
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc

%changelog
* Thu Feb 8 2013 Patrick Huang <pahuang@redhat.com> 9-1
- Initial RPM package
