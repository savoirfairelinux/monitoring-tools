%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           monitoring-plugins-sfl-check-http2
Version:        2014.7.18.16.15
Release:        1%{?dist}
Summary:        Checks HTTP sites, and doesn't timeout like good'old check_http.

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-check-http2_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
Checks HTTP sites, and doesn't timeout like good'old check_http.
More information is available on Github:
https://github.com/savoirfairelinux/sfl-shinken-plugins

%prep
%setup -q -n monitoring-plugins-sfl-check-http2


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
install -p -m0755 check_http2 %{buildroot}/%{_libdir}/monitoring/plugins/sfl

#%check
#cd %{buildroot}/%{python_sitelib}/shinkenplugins/plugins/ && %{__python} -c "import http2"


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/http2
%{_libdir}/monitoring/plugins/sfl/check_http2

%changelog
* Wed Dec 24 2014 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 0.2.0-1
- Initial package
