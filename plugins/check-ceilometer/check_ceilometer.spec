Name:		monitoring-plugins-sfl-check-ceilometer
Version:    	0.3.2
Release:    	1
License: 	GPL v3
Summary: 	Shinken plugin from SFL. A Nagios plug-in to use OpenStack Ceilometer API for metering
Group: 		Networking/Other
Source0: 	https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL:            https://github.com/savoirfairelinux/monitoring-tools
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Alexandre Viau <alexandre.viau@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
#Requires: python, python-dlnetsnmp

%description 
Shinken plugin from SFL. A Nagios plug-in to use OpenStack Ceilometer API for metering

%prep
%setup -q -n %{raw_name}

%pre
getent group shinken >/dev/null || /usr/sbin/groupadd -r shinken
getent passwd shinken >/dev/null || \
/usr/sbin/useradd -r -g shinken -d  %{_libdir}/shinken/ -s /bin/bash \
-c "Shinken user" shinken
exit 0

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/
%{__install} -d -m 755 %{buildroot}/%{_bindir}
%{__cp} -pr check_ceilometer %{buildroot}/%{_libdir}/shinken/plugins/check_ceilometer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, shinken, shinken, 0755)
%{_libdir}/shinken/
%defattr(0755, shinken, shinken, 0755)
%{_libdir}/shinken/plugins/check_ceilometer
%doc

%changelog
* Fri Jun 12 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com>
- Updated to 0.3.2

* Mon May 05 2014 Alexandre Viau <alexandre.viau@savoirfairelinux.com>
- Initial Release
