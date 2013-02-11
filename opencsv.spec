%if 0%{?fedora} > 18
    %define mvnbuildRequires maven-local
%else
    %define mvnbuildRequires maven
%endif

Name:           opencsv
Version:        2.1
Release:        1%{?dist}
Summary:        A Simple CSV Parser for Java

Group:          Development/Libraries
License:        Apache License V2.0
URL:            http://sourceforge.net/projects/%{name}
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}-src-with-libs.tar.gz

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
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  junit

Requires:       jpackage-utils
Requires:       java

%description
%{Summary}

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version} 
for j in $(find -name \*.jar); do
    if [ ! -L $j ] ; then
        rm $j
    fi
done
# disable gpg plugin
#%pom_remove_plugin :maven-gpg-plugin
%define mvn_opts -Dgpg.skip=true -Dproject.build.sourceEncoding=UTF-8
 
%build
mvn-rpmbuild package javadoc:aggregate %mvn_opts

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%check
mvn-rpmbuild verify %mvn_opts

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.1-1
- Initial RPM package
