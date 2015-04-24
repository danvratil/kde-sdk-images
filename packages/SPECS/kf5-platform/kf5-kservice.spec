%global framework kservice

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for advanced plugin and service introspection

License:        GPLv2+ and LGPLv2+
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev

BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kcrash-dev
BuildRequires:  kf5-kdbusaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kdoctools-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for advanced plugin and service
introspection.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-dev
Requires:       kf5-kcoreaddons-dev
Requires:       kf5-kdbusaddons-dev
Requires:       kf5-ki18n-dev

%description    dev
The %{name}-dev package contains libraries and header files for
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
%find_lang kservice5_qt --with-qt --all-name

mv %{buildroot}/%{_kf5_sysconfdir}/xdg/menus/applications.menu %{buildroot}/%{_kf5_sysconfdir}/xdg/menus/kf5-applications.menu

mkdir -p %{buildroot}/%{_kf5_datadir}/kservices5
mkdir -p %{buildroot}/%{_kf5_datadir}/kservicetypes5


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kservice5_qt.lang
%doc COPYING COPYING.LIB README.md
%config %{_kf5_sysconfdir}/xdg/menus/kf5-applications.menu
%{_kf5_bindir}/kbuildsycoca5
%{_kf5_libdir}/libKF5Service.so.*
%{_kf5_datadir}/kservicetypes5
%{_kf5_datadir}/kservices5
%{_kf5_mandir}/man8/*
%{_kf5_mandir}/*/man8/*
%exclude %{_kf5_mandir}/man8

%files dev
%{_kf5_includedir}/kservice_version.h
%{_kf5_includedir}/KService
%{_kf5_libdir}/libKF5Service.so
%{_kf5_libdir}/cmake/KF5Service
%{_kf5_archdatadir}/mkspecs/modules/qt_KService.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
