#
# Example spec file for cdplayer app...
#
%define raw_name    generic-redis
%define name        monitoring-packs-sfl-%{raw_name}
%define version     2015.1.29.16.52
%define release     1

Name:       %{name}
Version:    %{version}
Release:    %{release}%{?dist}
License: GPL v3
Summary: Pack for Redis server
Group: Networking/Other
Source: http://monitoring.savoirfairelinux.com/%{name}_%{version}.orig.tar.gz
URL: http://monitoring.savoirfairelinux.com/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Savoir-faire Linux <supervision@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
BuildRequires: python-sphinx
#Requires: python, python-dlnetsnmp

%description 
Pack for Redis server

%prep
%setup -q -n %{name}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}/%{_sysconfdir}/shinken/packs/%{raw_name}
%{__cp} -r pack/* %{buildroot}/%{_sysconfdir}/shinken/packs/%{raw_name}
%{__install} -p -m 755 package.json %{buildroot}/%{_sysconfdir}/shinken/packs/%{raw_name}
%{__install} -d -m 755 %{buildroot}/%{_docdir}/shinken/packs/%{raw_name}
%{__cp} -r doc/* %{buildroot}/%{_docdir}/shinken/packs/%{raw_name}
%{__rm} %{buildroot}/%{_docdir}/shinken/packs/%{raw_name}/conf.py
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/shinken/packs/%{raw_name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/%{raw_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%docdir
%{_docdir}/shinken/packs/%{raw_name}
%{_mandir}/man1/shinken/packs/%{raw_name}
%config
%{_sysconfdir}/shinken/packs/

%changelog
* Thu Jan 29 2015 Savoir-faire Linux <supervision@savoirfairelinux.com>
- Initial Release