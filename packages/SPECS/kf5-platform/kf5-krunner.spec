%global framework krunner

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution with parallelized query system

License:        LGPLv2+ and BSD
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/portingAids/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  kf5-kio-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-threadweaver-devel

Requires:       kf5-filesystem

%description
KRunner provides a parallelized query system extendable via plugins.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-plasma-devel
Requires:       qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5Runner.so.*
%{_kf5_qmldir}/org/kde/runnermodel
%{_kf5_datadir}/kservicetypes5/plasma-runner.desktop

%files devel
%doc
%{_kf5_includedir}/krunner_version.h
%{_kf5_includedir}/KRunner
%{_kf5_libdir}/libKF5Runner.so
%{_kf5_libdir}/cmake/KF5Runner
%{_kf5_archdatadir}/mkspecs/modules/qt_KRunner.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
