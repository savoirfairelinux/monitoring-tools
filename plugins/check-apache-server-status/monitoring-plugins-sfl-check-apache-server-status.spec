%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           monitoring-plugins-sfl-check-apache-server-status
Version:        2015.2.4.16.33
Release:        1%{?dist}
Summary:        Get Apache metrics from mod_status Apache status

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-apache-server-status_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
Get Apache metrics from mod_status Apache status
More information is available on Github:
https://github.com/savoirfairelinux/sfl-shinken-plugins

%prep
%setup -q -n monitoring-plugins-sfl-check-apache-server-status


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -p -m0755 check_apache_server_status %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -d -m 755 %{buildroot}/%{_docdir}/shinken/plugins/%{name}
%{__cp} -r doc/source/ %{buildroot}/%{_docdir}/shinken/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/shinken/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/shinken/plugins/%{name}

#%check
#cd %{buildroot}/%{python_sitelib}/shinkenplugins/plugins/ && %{__python} -c "import apache_server_status"


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/apache_server_status
%{_libdir}/monitoring/plugins/sfl/check_apache_server_status
%docdir
%{_docdir}/shinken/plugins/%{name}
%{_mandir}/man1/shinken/plugins/%{name}

%changelog
* Wed Feb 04 2015 Savoir-faire Linux <supervision@savoirfairelinux.com> - 2015.2.4.16.33
- Initial package