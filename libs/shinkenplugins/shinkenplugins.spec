%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           python-shinkenplugins
Version:        0.2.0
Release:        1%{?dist}
Summary:        Shinken plugins wrapper library

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/shinkenplugins_%{version}.orig.tar.gz

Requires:       python
BuildRequires:  python-setuptools
BuildRequires:  gcc
BuildRequires:  python-devel

BuildArch:      noarch


%description
Library aimed to provide helpers around the creation of Shinken
plugins, and in particular their inputs and outputs. Less code,
less code duplication, less headache. More lolz.


%prep
%setup -q -n shinkenplugins


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}


%check
PYTHONPATH=. %{__python} -c "import shinkenplugins"


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/*


%changelog
* Wed Dec 24 2014 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 0.2.0-1
- Initial package
