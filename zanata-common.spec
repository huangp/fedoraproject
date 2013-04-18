%global shortname common

%global submodule_util zanata-%{shortname}-util
%global submodule_po zanata-adapter-po
%global submodule_properties zanata-adapter-properties
%global submodule_xliff zanata-adapter-xliff
%global submodule_glossary zanata-adapter-glossary

Name:           zanata-%{shortname}
Version:        2.2.1
Release:        1%{?dist}
Summary:        Zanata common modules

Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/zanata/%{name}
Source0:        https://github.com/zanata/%{name}/archive/%{shortname}-%{version}.zip

BuildArch:      noarch

BuildRequires:	maven-local 

BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-provider-testng

# dependencies in pom
BuildRequires:  zanata-parent
BuildRequires:	zanata-api
BuildRequires:	slf4j
BuildRequires:  testng
BuildRequires:  hamcrest

# dependencies in zanata-common-util
BuildRequires:	jackson
BuildRequires:	guava
BuildRequires:	apache-commons-io
BuildRequires:	apache-commons-codec
BuildRequires:  junit

# dependencies in zanata-adapter-po
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

%description
Zanata common modules

%package -n %{submodule_util}
Summary:        Zanata common utility module
Requires:       jackson
Requires:       guava
Requires:       apache-commons-io
Requires:       apache-commons-codec

%description -n %{submodule_util}
%{Summary}

%package -n %{submodule_po}
Summary:        PO reader and writer
Requires:       jgettext
Requires:       apache-commons-lang

%description -n %{submodule_po}
%{summary}

%package -n %{submodule_properties}
Summary:        Properties reader and writer
Requires:       openprops

%description -n %{submodule_properties}
%{summary}

%package -n %{submodule_xliff}
Summary:        xliff reader and writer

%description -n %{submodule_xliff}
%{summary}

%package -n %{submodule_glossary}
Summary:        glossary reader and writer
Requires:       opencsv

%description -n %{submodule_glossary}
%{summary}

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
%mvn_build -s

%install
%mvn_install

%files -f .mfiles
%doc README.txt COPYING.LESSER COPYING.GPL

%files -f .mfiles-%{shortname}
%files -n %{submodule_util} -f .mfiles-%{submodule_util}
%files -n %{submodule_po} -f .mfiles-%{submodule_po}
%files -n %{submodule_properties} -f .mfiles-%{submodule_properties}
%files -n %{submodule_xliff} -f .mfiles-%{submodule_xliff}
%files -n %{submodule_glossary} -f .mfiles-%{submodule_glossary}

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Mar 19 2013 Patrick Huang <pahuang@redhat.com> 2.2.1-1
- Upstream version update

* Thu Feb 28 2013 Patrick Huang <pahuang@redhat.com> 2.2.0-1
- Upstream version update

* Mon Feb 11 2013 Patrick Huang <pahuang@redhat.com> 2.1.1-1
- Initial RPM package
