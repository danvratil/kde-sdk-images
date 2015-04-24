Name:           kf5-sdk-base
Version:        0.1
Release:        1%{?dist}
Summary:        Qt 5 sdk base

License:        Various
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

BuildRequires:  qt5-sdk-base

Requires:       qt5-sdk-base

%description
Base package for building KF5 SDK

%prep

%build

%files

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
