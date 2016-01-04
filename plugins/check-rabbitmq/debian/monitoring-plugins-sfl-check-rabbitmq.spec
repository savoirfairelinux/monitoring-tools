%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           monitoring-plugins-sfl-check-rabbitmq
Version:        2015.12.17.14.35
Release:        1%{?dist}
Summary:        Verify good behavior of a RabbitMQ exchange and queue

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-rabbitmq_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
Verify good behavior of a RabbitMQ exchange and queue
More information is available on Github:
https://github.com/savoirfairelinux/sfl-monitoring-tools

%prep
%setup -q -n monitoring-plugins-sfl-check-rabbitmq


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -p -m0755 check_rabbitmq %{buildroot}/%{_libdir}/monitoring/plugins/sfl
%{__install} -d -m 755 %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__cp} -r doc/source/ %{buildroot}/%{_docdir}/monitoring/plugins/%{name}
%{__install} -d -m 755 %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/monitoring/plugins/%{name}


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/rabbitmq
%{_libdir}/monitoring/plugins/sfl/check_rabbitmq
%docdir
%{_docdir}/monitoring/plugins/%{name}
%{_mandir}/man1/monitoring/plugins/%{name}

%changelog
* Thu Dec 17 2015 Grégory Starck <g.starck@gmail.com> - 2015.12.17.14.35
- Initial package