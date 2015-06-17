%define raw_name   check-keystone
%define name       monitoring-plugins-sfl-%{raw_name}
%define version    0.4.0
%define release    1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Alignak plugin to check Keystone
Group:          Networking/Other

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
Requires:       python-keystoneclient

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

BuildArch:      noarch

%description
Alignak plugin from SFL. A Nagios plug-in to check OpenStack Keystone.
More information is available on Github:
https://github.com/savoirfairelinux/sfl-monitoring-tools

%prep
%setup -q


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__ln_s} %{_libdir}/monitoring/plugins/sfl/check_keystone  %{buildroot}/%{_libdir}/monitoring/plugins/sfl/check_keystone


%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__cp} -r doc/ %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/plugins/%{name}


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%{python_sitelib}/shinkenplugins.plugins.keystone-1.0-py2.7-nspkg.pth
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/keystone
%{_bindir}/check_keystone
%{_libdir}/monitoring/plugins/sfl/check_keystone

%docdir
%{_docdir}/monitoring/plugins/%{name}
%{_mandir}/man1/monitoring/plugins/%{name}

%changelog
* Wed Jun 17 2015 Vincent Fournier <vincent.fournier@savoirfairelinux.com> 0.4.0-1
- Update to version 0.4.0-1

* Mon May 05 2014 Alexandre Viau <alexandre.viau@savoirfairelinux.com>
- Initial Release
