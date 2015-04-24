%global framework networkmanager-qt

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        A Tier 1 KDE Frameworks 5 module that wraps NetworkManager DBus API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://projects.kde.org/projects/frameworks/networkmanager-qt

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

BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
BuildRequires:  pkgconfig(libnm)
%else
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)
%endif

Requires:       NetworkManager >= 0.9.9.0
Requires:       kf5-filesystem

%description
A Tier 1 KDE Frameworks 5 Qt library for NetworkManager.

%package dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-dev
%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
Requires:       pkgconfig(libnm)
%else
Requires:       pkgconfig(libnm-glib) pkgconfig(libnm-util)
%endif

%description    dev
Qt libraries and header files for developing applications
that use NetworkManager.

%prep
%setup -qn %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5NetworkManagerQt.so.*

%files dev
%{_kf5_libdir}/libKF5NetworkManagerQt.so
%{_kf5_libdir}/cmake/KF5NetworkManagerQt
%{_kf5_includedir}/NetworkManagerQt
%{_kf5_includedir}/networkmanagerqt_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_NetworkManagerQt.pri

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
