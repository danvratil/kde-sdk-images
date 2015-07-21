Name:           extra-cmake-modules
Summary:        Additional modules for CMake build system
Version:        5.9.0
Release:        1%{?dist}

License:        BSD
URL:            http://community.kde.org/KDE_Core/Platform_11/Buildsystem/FindFilesSurvey

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  kf5-sdk-base

Requires:       kf5-sdk-base

%description
Additional modules for CMake build system needed by KDE Frameworks.


%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files
%doc README.rst COPYING-CMAKE-SCRIPTS
%{_datadir}/ECM

%changelog
