Name:           qt5-sdk
Version:        0.1
Release:        1%{?dist}
Summary:        Qt 5 sdk
Source1:        rpm-macros

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: qt5-platform

Requires: qt5-platform
Requires: freedesktop-sdk

Requires: qt5-qtbase-dev

%description
Meta package for Gnome SDK dependencies

%prep


%build

%files
%{_libdir}/debug/self

%changelog
* Mon Apr 20 2015 Daniel Vrátil <dvratil@redhat.com>
- Initial version
