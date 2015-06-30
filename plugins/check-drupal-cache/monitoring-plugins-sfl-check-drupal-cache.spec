%define raw_name       check-drupal-cache
%define name           monitoring-plugins-sfl-%{raw_name}
%define version        0.1.0
%define release        1
%define command_name   check_drupal_cache

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Alignak plugin to check the Drupal cache service
Group:          Networking/Other

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/%{name}-%{version}.orig.tar.gz

Requires:       python-shinkenplugins

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

BuildArch:      noarch

%description
Alignak plugin to check the Drupal cache service
More information is available on Github:
https://github.com/savoirfairelinux/monitoring-tools

%prep
%setup -q


%build
%{__python} setup.py build

%install
# Install command
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__ln_s} %{_bindir}/%{command_name}  %{buildroot}/%{_libdir}/monitoring/plugins/sfl/%{command_name}

# Install documentation
%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/sfl/%{raw_name}
%{__cp} -r doc/ %{buildroot}/%{_docdir}/monitoring/plugins/sfl/%{raw_name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/plugins/sfl/%{raw_name}

# Remove useless files
%{__rm} -rf %{buildroot}/%{python_sitelib}/shinkenplugins.plugins.*egg-info/
%{__rm} -f %{buildroot}/%{python_sitelib}/shinkenplugins.plugins.*-nspkg.pth

%files
%defattr(-,root,root,-)

%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/
%{_bindir}/%{command_name}
%{_libdir}/monitoring/plugins/sfl/%{command_name}

%docdir
%{_docdir}/monitoring/plugins/sfl/%{raw_name}
%{_mandir}/man1/%{command_name}.1.gz



%changelog
* Tue Jun 30 2015 Frédéric Vachon <frederic.vachon@savoirfairelinux.com> - 2015.6.30.11.11
- Initial package
