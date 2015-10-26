#
# Example spec file for cdplayer app...
#
%define raw_name    generic-rabbitmq-http
%define name        monitoring-packs-sfl-%{raw_name}
%define version     2015.10.23.12.8
%define release     1

Name:       %{name}
Version:    %{version}
Release:    %{release}
License: GPL v3
Summary: Pack to monitor rabbitmq server through the HTTP API
Group: Networking/Other
Source: https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL: https://github.com/savoirfairelinux/monitoring-tools/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
#%{?el7:BuildRequires: python-sphinx}
#Requires: python, python-dlnetsnmp


%description
Pack to monitor rabbitmq server through the HTTP API

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
* Fri Oct 23 2015 Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
- Initial Release