%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%define raw_name    check-redis
%define name        monitoring-packs-sfl-%{raw_name}
%define version     2015.2.17.14.15
%define release     1


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Check Redis database

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-redis_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools
BuildRequires:  gcc
BuildRequires:  python-dev
#%{?el7:BuildRequires: python-sphinx}

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
%{__mv} %{buildroot}/usr/bin/*  %{buildroot}/%{_libdir}/monitoring/plugins/sfl/
%{__rm} -rf %{buildroot}/usr/bin/
find %{buildroot}/%{python_sitelib} -name "*.py[co]" -exec rm {} \;

sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/plugins/%{raw_name}

sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man1/

%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/shinkenplugins/plugins
%{_libdir}/monitoring/plugins/sfl/check_redis
%doc
%{_docdir}/monitoring/plugins/%{raw_name}
%{_mandir}/man1/*

%changelog
* Fri Feb 20 2015 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 2015.2.17.14.15-1
- Initial package
