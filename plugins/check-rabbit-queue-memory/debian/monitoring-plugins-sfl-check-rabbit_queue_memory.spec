%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           monitoring-plugins-sfl-check-rabbit-queue-memory
Version:        2016.4.28.13.31
Release:        1%{?dist}
Summary:        Check the memory used by a rabbitmq queue

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-rabbit-queue-memory_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
Check the memory used by a rabbitmq queue
More information is available on Github:
https://github.com/savoirfairelinux/sfl-monitoring-tools

%prep
%setup -q -n monitoring-plugins-sfl-check-rabbit-queue-memory


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -p -m0755 check_rabbit_queue_memory %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__cp} -r doc/source/ %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/rabbit_queue_memory
%{_libdir}/monitoring/plugins/sfl/check_rabbit_queue_memory
%docdir
%{_docdir}/monitoring/plugins/%{name}
%{_mandir}/man1/monitoring/plugins/%{name}

%changelog
* Thu Apr 28 2016 Flavien Peyre <flavien.peyre@savoirfairelinux.com> - 2016.4.28.13.31
- Initial package