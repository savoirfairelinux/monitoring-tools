Name:           monitoring-plugins-sfl-check-ceilometer
Version:        0.4.0
Release:        1
Summary:        Alignak plugin from SFL. A Nagios plug-in to use OpenStack Ceilometer API for metering
Group:          Networking/Other

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-ceilometer_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
Requires:       python-ceilometerclient
Requires:       python-keystoneclient

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

BuildArch:      noarch

%description
Shinken plugin from SFL. A Nagios plug-in to use OpenStack Ceilometer API for metering
More information is available on Github:
https://github.com/savoirfairelinux/sfl-monitoring-tools

%prep
%setup -q


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__ln_s} %{_libdir}/monitoring/plugins/sfl/check_ceilometer  %{buildroot}/%{_libdir}/monitoring/plugins/sfl/check_ceilometer


%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__cp} -r doc/ %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/plugins/%{name}


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%{python_sitelib}/shinkenplugins.plugins.ceilometer-1.2-py2.7-nspkg.pth
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/ceilometer
%{_bindir}/check_ceilometer
%{_libdir}/monitoring/plugins/sfl/check_ceilometer

%docdir
%{_docdir}/monitoring/plugins/%{name}
%{_mandir}/man1/monitoring/plugins/%{name}

%changelog
* Wed Jun 17 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com> 0.4.0-1
- Update to version 0.4.0-1

* Mon May 05 2014 Alexandre Viau <alexandre.viau@savoirfairelinux.com>
- Initial Release
