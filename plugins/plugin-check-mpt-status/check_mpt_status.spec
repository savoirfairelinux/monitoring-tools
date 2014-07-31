#
# Example spec file for cdplayer app...
#
%define raw_name    check_mpt_status
%define name        check-mpt-status
%define version     20130322
%define release     1
%define install_folder /usr/lib/

Name:       %{name}
Version:    %{version}
Release:    %{release}.%{dist}
License: GPL v3
Summary: Shinken plugin from SFL. Check mpt HW RAID controllers status
Group: Networking/Other
Source: https://github.com/savoirfairelinux/plugin-%{raw_name}/archive/master.tar.gz
URL: https://github.com/savoirfairelinux/sfl-shinken-plugins
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
Requires: mpt-status

%description 
Shinken plugin from SFL. Check mpt HW RAID controllers status

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
%{__cp} -pr check_mpt_status %{buildroot}/%{_libdir}/shinken/plugins/check_mpt_status

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, shinken, shinken, 0755)
%{_libdir}/shinken/
%defattr(0755, shinken, shinken, 0755)
%{_libdir}/shinken/plugins/check_mpt_status
%doc

%changelog
* Fri Mar 22 2013 Thibault Cohen <thibault.cohen@savoirfairelinux.com>
- Initial Release
