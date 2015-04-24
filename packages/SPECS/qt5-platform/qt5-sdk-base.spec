Name:           qt5-sdk-base
Version:        0.1
Release:        1%{?dist}
Summary:        Qt 5 sdk base
Source1:        macros.cmake

License:        Various
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

BuildRequires:  freedesktop-sdk-base

Requires:       freedesktop-sdk-base

%description
Base package for building Qt5 SDK

%prep

%build
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.cmake

%files
%{_rpmconfigdir}/macros.d/macros.cmake

%changelog
* Mon Apr 20 2015 Daniel Vrátil <dvratil@redhat.com>
- Initial version
