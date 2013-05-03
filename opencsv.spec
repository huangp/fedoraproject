Name:           opencsv
Version:        2.3
Release:        6%{?dist}
Summary:        A very simple csv (comma-separated values) parser library for Java
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://opencsv.sourceforge.net/
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}-src-with-libs.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  maven-local

BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  junit

Requires:       jpackage-utils
Requires:       java

%description
Support for all the basic csv-type things you're likely to want to do.


%package javadoc
Summary:           Javadocs for %{name}
Group:             Documentation
Requires:          jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q # -n %{name}-%{version}

### making sure we dont use it
rm -rf lib/* doc deploy

%{__sed} -i 's/\r//' examples/MockResultSet.java
%{__sed} -i 's/\r//' examples/JdbcExample.java
%{__sed} -i 's/\r//' examples/addresses.csv
%{__sed} -i 's/\r//' examples/AddressExample.java

%build
# skip test because it is not jdk 1.6 compatible 
#%global mvn_opts -Dgpg.skip=true -Dproject.build.sourceEncoding=UTF-8 -Dmaven.test.skip=true
#mvn-rpmbuild package javadoc:aggregate %mvn_opts 
%mvn_build --skip-tests

%install
%mvn_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc examples

%files -f .mfiles-javadoc


%changelog
* Tue Apr 30 2013 Patrick Huang <pahuang@redhat.com> - 2.3-6
- Adapte latest java packaging guideline

* Fri Mar 1 2013 Patrick Huang <pahuang@redhat.com> - 2.3-5
- Change to build by maven

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Sandro Mathys <red at fedoraproject.org> - 2.3-1
- New upstream version 2.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 26 2010 Sandro Mathys <red at fedoraproject.org> - 2.2-2
- rebuilt

* Mon Apr 26 2010 Sandro Mathys <red at fedoraproject.org> - 2.2-1
- update to upstream version 2.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Sandro Mathys <red at fedoraproject.org> - 1.8-2
- Examples now docs
- Removed feature list in description
- Added symlink to the javadocs (name-version -> name)

* Tue Dec 16 2008 Sandro Mathys <red at fedoraproject.org> - 1.8-1
- initial build (thanks Rudolf 'che' Kastl for the help)
