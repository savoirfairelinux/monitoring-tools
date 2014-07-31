#
# Example spec file for cdplayer app...
#
%define raw_name    check_reactionner_health
%define name        check-reactionner-health
%define version     20140204
%define release     1
%define install_folder /usr/lib/

Name:       %{name}
Version:    %{version}
Release:    %{release}.%{dist}
License: GPL v3
Summary: Shinken plugin from SFL. Pseudo crontab to check if a file is edited by shinken reactionner
Group: Networking/Other
Source: http://monitoring.savoirfairelinux.com/%{name}.tar.gz
URL: http://monitoring.savoirfairelinux.com/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
#Requires: python, python-dlnetsnmp

%description 
Shinken plugin from SFL. Pseudo crontab to check if a file is edited by shinken reactionner

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
%{__cp} -pr check_reactionner_health %{buildroot}/%{_libdir}/shinken/plugins/check_reactionner_health

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, shinken, shinken, 0755)
%{_libdir}/shinken/
%defattr(0755, shinken, shinken, 0755)
%{_libdir}/shinken/plugins/check_reactionner_health
%doc

%changelog
* Tue Feb 04 2014 Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
- Initial Release
