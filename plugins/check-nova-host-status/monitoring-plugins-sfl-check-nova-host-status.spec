Name:           monitoring-plugins-sfl-check-nova-host-status
Version:        0.4.0
Release:        1
Summary:        check the current status for a nova host

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-nova-host-status_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
Requires:	python-novaclient

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

BuildArch:      noarch

%description
check the current status for a nova host
More information is available on Github:
https://github.com/savoirfairelinux/sfl-monitoring-tools

%prep
%setup -q 


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} 
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__ln_s} %{_libdir}/monitoring/plugins/sfl/check_nova_host_status %{buildroot}/%{_libdir}/monitoring/plugins/sfl/check_nova_host_status

%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__cp} -r doc/ %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/plugins/%{name}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%{python_sitelib}/shinkenplugins.plugins.nova_host_status-1.0-py2.7-nspkg.pth
%{_bindir}/check_nova_host_status
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/nova_host_status
%{_libdir}/monitoring/plugins/sfl/check_nova_host_status

%docdir
%{_docdir}/monitoring/plugins/%{name}
%{_mandir}/man1/monitoring/plugins/%{name}

%changelog
* Wed Jun 17 2015 Flavien Peyre <peyre.flavien@gmail.com> - 0.4.0-1
- Update to version 0.4.0 

* Fri May 29 2015 Flavien Peyre <peyre.flavien@gmail.com> - 2015.5.29.13.21
- Initial package
