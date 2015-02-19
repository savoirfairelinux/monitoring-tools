#
# Example spec file for cdplayer app...
#
%define raw_name    generic-multisite-http
%define name        monitoring-packs-sfl-%{raw_name}
%define version     2015.2.19.16.42
%define release     1

Name:       %{name}
Version:    %{version}
Release:    %{release}
License: GPL v3
Summary: CheckMK Multisite active checks with HTTP requests
Group: Networking/Other
Source: https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL: https://github.com/savoirfairelinux/monitoring-tools/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Savoir-faire Linux <supervision@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
#%{?el7:BuildRequires: python-sphinx}
#Requires: python, python-dlnetsnmp


%description 
CheckMK Multisite active checks with HTTP requests

%prep
%setup -q

%build
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man7/%{raw_name}
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/packs/%{raw_name}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}/%{_libdir}/monitoring/packs/%{raw_name}
%{__cp} -r pack/* %{buildroot}/%{_libdir}/monitoring/packs/%{raw_name}
%{__install} -p -m 755 package.json %{buildroot}/%{_libdir}/monitoring/packs/%{raw_name}
%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/packs/%{raw_name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man7/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_libdir}/monitoring/packs/
%doc
%{_docdir}/monitoring/packs/%{raw_name}
%{_mandir}/man7/%{name}


%changelog
* Thu Feb 19 2015 Savoir-faire Linux <supervision@savoirfairelinux.com>
- Initial Release