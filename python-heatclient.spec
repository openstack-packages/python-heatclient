%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:    python-heatclient
Version: 1.0.0
Release: 1%{?dist}
Summary: Python API and CLI for OpenStack Heat

Group:   Development/Languages
License: ASL 2.0
URL:     http://pypi.python.org/pypi/python-heatclient
Source0: http://tarballs.openstack.org/%{name}/%{name}-%{version}%{?milestone}.tar.gz

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr

Requires: python-argparse
Requires: python-httplib2
Requires: python-iso8601
Requires: python-keystoneclient
Requires: python-prettytable
Requires: python-pbr
Requires: python-six
Requires: python-oslo-serialization
Requires: python-oslo-utils
Requires: python-oslo-i18n
Requires: PyYAML

%description
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

%package doc
Summary: Documentation for OpenStack Heat API Client
Group:   Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: git

%description doc
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config.
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
echo "%{version}" > %{buildroot}%{python2_sitelib}/heatclient/versioninfo

# Install bash completion scripts
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -m 644 -T tools/heat.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/python-heatclient

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/heatclient/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/heat
%{python2_sitelib}/heatclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/python-heatclient

%files doc
%doc html

%changelog
* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 1.0.0-0.1
 -  Rebuild for Mitaka 
