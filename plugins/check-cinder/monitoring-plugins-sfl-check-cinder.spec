%define raw_name       check-cinder
%define name           monitoring-plugins-sfl-%{raw_name}
%define version        0.4.0
%define release        1
%define command_name   check_cinder

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Alignak plugin to check the OpenStack cinder service
Group:          Networking/Other

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
Requires:	python-keystoneclient
Requires:	python-requests

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

BuildArch:      noarch

%description
Alignak plugin to check the OpenStack cinder service
More information is available on Github:
https://github.com/savoirfairelinux/sfl-monitoring-tools

%prep
%setup -q


%build
%{__python} setup.py build

%install
# Install command
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir_p} %{buildroot}/usr/lib/monitoring/plugins/sfl/
%{__ln_s} %{_bindir}/%{command_name}  %{buildroot}/usr/lib/monitoring/plugins/sfl/%{command_name}

# Install documentation
%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/sfl/%{raw_name}
%{__cp} -r doc/ %{buildroot}/%{_docdir}/monitoring/plugins/sfl/%{raw_name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/plugins/sfl/%{raw_name}

%files
%defattr(-,root,root,-)

%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/
%{python_sitelib}/shinkenplugins.plugins.*egg-info
%{python_sitelib}/shinkenplugins.plugins.*-nspkg.pth
%{_bindir}/%{command_name}
/usr/lib/monitoring/plugins/sfl/%{command_name}

%docdir
%{_docdir}/monitoring/plugins/sfl/%{raw_name}
%{_mandir}/man1/%{command_name}.1.gz

%changelog
* Wed Jun 17 2015 Flavien Peyre <peyre.flavien@gmail.com> - 0.4.0-1
- Update to version 0.4.0 

* Fri May 29 2015 Flavien Peyre <peyre.flavien@gmail.com> - 2015.5.29.13.21
- Initial package

