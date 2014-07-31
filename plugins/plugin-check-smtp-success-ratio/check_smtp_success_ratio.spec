#
# Example spec file for cdplayer app...
#
%define raw_name    check_smtp_success_ratio
%define name        check-smtp-success-ratio
%define version     20130307
%define release     1
%define install_folder /usr/lib/

Name:       %{name}
Version:    %{version}
Release:    %{release}.%{dist}
License: GPL v3
Summary: Shinken plugin from SFL. Given a maillog, checks for a good ratio of sent versus total emails.
Group: Networking/Other
Source: http://monitoring.savoirfairelinux.com/%{name}.tar.gz
URL: http://monitoring.savoirfairelinux.com/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
#Requires: python, python-dlnetsnmp

%description 
Shinken plugin from SFL. Given a maillog, checks for a good ratio of sent versus total emails.

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
%{__cp} -pr check_smtp_success_ratio.inc %{buildroot}/%{_libdir}/shinken/plugins/check_smtp_success_ratio.inc
%{__cp} -pr check_smtp_success_ratio %{buildroot}/%{_libdir}/shinken/plugins/check_smtp_success_ratio

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, shinken, shinken, 0755)
%{_libdir}/shinken/
%defattr(0755, shinken, shinken, 0755)
%{_libdir}/shinken/plugins/check_smtp_success_ratio.inc
%{_libdir}/shinken/plugins/check_smtp_success_ratio
%doc

%changelog
* Thu Mar 07 2013 Stéphane Duchesneau <stephane.duchesneau@savoirfairelinux.com>
- Initial Release
