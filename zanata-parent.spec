%global shortname parent

Name:           zanata-%{shortname}
Version:        12
Release:        1%{?dist}
Summary:        The Project Object Model(pom) files for the Zanata packages

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{name}-%{version}.zip

BuildArch:      noarch

BuildRequires:  maven-local

BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  resteasy

Requires:       jpackage-utils
Requires:       java

%description
The Project Object Model(pom) files for the Zanata packages.

%prep
%setup -q -n %{name}-%{name}-%{version}
# disable some plugins that are not in fedora and not relevant in fedora packaging 
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :versions-maven-plugin
%pom_remove_plugin :maven-eclipse-plugin

# we have to remove wagon-webdav-jackrabbit until jackrabbit is available
%pom_xpath_remove "pom:build/pom:extensions"

%build
%if 0%{?fedora} >= 19
%mvn_build
%else
mvn-rpmbuild install
%endif

%install

%if 0%{?fedora} >= 19
%mvn_install
%else
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom
%endif

%files -f .mfiles
%doc README.txt COPYING.LESSER COPYING.GPL

%changelog
* Mon Apr 29 2013 Patrick Huang <pahuang@redhat.com> 12-1
- latest upstream version

* Tue Mar 19 2013 Patrick Huang <pahuang@redhat.com> 11-3
- change according to new java packaging guideline

* Tue Mar 12 2013 Patrick Huang <pahuang@redhat.com> 11-2
- disable a few plugins that are not relevant in fedora packaging

* Wed Mar 6 2013 Patrick Huang <pahuang@redhat.com> 11-1
- upstream version upgrade

* Wed Mar 6 2013 Patrick Huang <pahuang@redhat.com> 10-2
- add licenses

* Tue Feb 26 2013 Patrick Huang <pahuang@redhat.com> 10-1
- upstream upgrade to version 10

* Fri Feb 8 2013 Patrick Huang <pahuang@redhat.com> 9-1
- Initial RPM package
