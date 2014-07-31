#
# Example spec file for cdplayer app...
#
%define raw_name    requests
%define name        python-requests
%define version     20130218
%define release     1
%define install_folder /usr/lib/

Name:       %{name}
Version:    %{version}
Release:    %{release}.%{dist}
License: GPL v3
Summary: Requests SFL lib
Group: Networking/Other
Source: https://github.com/savoirfairelinux/sfl-shinken-plugins%{raw_name}.tar.gz
URL: https://github.com/savoirfairelinux/sfl-shinken-plugins
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Thibault Cohen <thibault.cohen@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
Requires: pythona >= 2.5

%description 
Python requests SFL lib

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
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/charade
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/urllib3
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/urllib3/packages
%{__install} -d -m 755 %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/urllib3/packages/ssl_match_hostname
%{__cp} -pr *.py %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}
%{__cp} -pr packages/*.py %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages
%{__cp} -pr packages/charade/*.py %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/charade
%{__cp} -pr packages/urllib3/*.py %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/urllib3
%{__cp} -pr packages/urllib3/packages/*.py %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/urllib3/packages
%{__cp} -pr packages/urllib3/packages/ssl_match_hostname/*.py %{buildroot}/%{_libdir}/shinken/plugins/%{raw_name}/packages/urllib3/packages/ssl_match_hostname

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, shinken, shinken, 0755)
%{_libdir}/shinken/plugins/%{raw_name}
%doc

%changelog
* Mon Feb 18 2013 Thibault Cohen <thibault.cohen@savoirfairelinux.com>
- Initial Release
