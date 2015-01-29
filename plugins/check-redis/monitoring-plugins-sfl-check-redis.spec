%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           monitoring-plugins-sfl-check-redis
Version:        2014.7.18.16.15
Release:        1%{?dist}
Summary:        Check Redis database

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-redis_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools, python-sphinx

BuildArch:      noarch

%description
Check Redis database
More information is available on Github:
https://github.com/savoirfairelinux/sfl-shinken-plugins

%prep
%setup -q -n monitoring-plugins-sfl-check-redis


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -p -m0755 check_redis %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -d -m 755 %{buildroot}/%{_docdir}/shinken/plugins/%{name}
%{__cp} -r doc/source/ %{buildroot}/%{_docdir}/shinken/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/shinken/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/shinken/plugins/%{name}


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/redis
%{_libdir}/monitoring/plugins/sfl/check_redis
%docdir
%{_docdir}/shinken/plugins/%{name}
%{_mandir}/man1/shinken/plugins/%{name}

%changelog
* Wed Dec 24 2014 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 0.2.0-1
- Initial package
