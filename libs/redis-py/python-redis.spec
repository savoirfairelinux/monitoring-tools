%if 0%{?fedora} >= 13 || 0%{?el} >= 8
%global with_python3 1
%endif

%global upstream_name redis

Name:           python-%{upstream_name}
Version:        2.10.3
Release:        1%{?dist}
Summary:        Python 2 interface to the Redis key-value store
License:        MIT
URL:            http://github.com/andymccurdy/redis-py
Source0:        http://pypi.python.org/packages/source/r/redis/redis-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-py
BuildRequires:  pytest
BuildRequires:  redis

%description
This is a Python 2 interface to the Redis key-value store.

%if 0%{?with_python3}
%package -n     python3-redis
Summary:        Python 3 interface to the Redis key-value store
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-py
BuildRequires:  python3-pytest

%description -n python3-redis
This is a Python 3 interface to the Redis key-value store.
%endif

%prep
%setup -qn %{upstream_name}-%{version}
rm -frv %{upstream_name}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif
%{__python2} setup.py build

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check
#redis-server &
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif
#%{__python2} setup.py test
#kill %1

%files
%doc CHANGES LICENSE README.rst
%{python2_sitelib}/%{upstream_name}
%{python2_sitelib}/%{upstream_name}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-redis
%doc CHANGES LICENSE README.rst
%{python3_sitelib}/%{upstream_name}
%{python3_sitelib}/%{upstream_name}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Thu Aug 21 2014 Christopher Meng <rpm@cicku.me> - 2.10.3-1
- Update to 2.10.3

* Tue Aug 12 2014 Christopher Meng <rpm@cicku.me> - 2.10.2-1
- Update to 2.10.2

* Thu Jun 19 2014 Christopher Meng <rpm@cicku.me> - 2.10.1-1
- Update to 2.10.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Feb 14 2014 Christopher Meng <rpm@cicku.me> - 2.9.1-1
- Update to 2.9.1
- Use generated egg instead of bundled egg
- Cleanup again

* Sat Jul 27 2013 Luke Macken <lmacken@redhat.com> - 2.7.6-1
- Update to 2.7.6
- Run the test suite
- Add a python3 subpackage
- Remove obsolete buildroot tag and cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Silas Sewell <silas@sewell.org> - 2.7.2-1
- Update to 2.7.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 2.4.9-1
- Update to 2.4.9

* Sun Mar 27 2011 Silas Sewell <silas@sewell.ch> - 2.2.4-1
- Update to 2.2.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Initial build
