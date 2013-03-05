%global shortname parent

Name:           zanata-%{shortname}
Version:        10
Release:        2%{?dist}
Summary:        The Project Object Model(pom) files for the Zanata packages

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{name}-%{version}.zip
Source1:        http://www.gnu.org/licenses/gpl-2.0.txt
Source2:        http://www.gnu.org/licenses/lgpl-2.1.txt

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
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  resteasy

Requires:       jpackage-utils
Requires:       java

%description
The Project Object Model(pom) files for the Zanata packages.

%prep
%setup -q -n %{name}-%{name}-%{version}
# disable maven enforcer
%pom_remove_plugin :maven-enforcer-plugin
# we have to remove wagon-webdav-jackrabbit until jackrabbit is available

cp -p %{SOURCE1} ./COPYING.LESSER
cp -p %{SOURCE2} ./COPYING.GPL

%build

mvn-rpmbuild install

%install
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom

%files -f .mfiles
%doc README.txt COPYING.LESSER COPYING.GPL

%changelog
* Wed Mar 6 2013 Patrick Huang <pahuang@redhat.com> 10-2
- add licenses

* Tue Feb 26 2013 Patrick Huang <pahuang@redhat.com> 10-1
- upstream upgrade to version 10

* Thu Feb 8 2013 Patrick Huang <pahuang@redhat.com> 9-1
- Initial RPM package
