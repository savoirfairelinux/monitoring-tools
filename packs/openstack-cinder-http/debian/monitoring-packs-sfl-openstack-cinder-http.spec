%define raw_name    openstack-cinder-http
%define name        monitoring-packs-sfl-%{raw_name}
%define version     0.4.0
%define release     1

Name:       %{name}
Version:    %{version}
Release:    %{release}
License: GPL v3
Summary: Alignak pack for monitoring Openstack cinder
Group: Networking/Other
Source: https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL: https://github.com/savoirfairelinux/monitoring-tools/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Savoir-faire Linux <supervision@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
BuildRequires: python-sphinx
#Requires: python, python-dlnetsnmp


%description
Alignak pack for monitoring Openstack cinder

%prep
%setup -q

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}/%{_datadir}/monitoring/packs/sfl/%{raw_name}
%{__cp} -r pack/* %{buildroot}/%{_datadir}/monitoring/packs/sfl/%{raw_name}
%{__install} -p -m 755 package.json %{buildroot}/%{_datadir}/monitoring/packs/sfl/%{raw_name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man7/%{raw_name}
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/packs/sfl/%{raw_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/monitoring/packs/sfl
%doc
%{_docdir}/monitoring/packs/sfl/%{raw_name}
%{_mandir}/man7/*


%changelog
* Tue Jun 16 2015 Savoir-faire Linux <supervision@savoirfairelinux.com>
- Initial Release
