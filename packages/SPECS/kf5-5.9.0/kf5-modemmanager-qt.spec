%global framework modemmanager-qt

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        A Tier 1 KDE Frameworks module wrapping ModemManager DBus API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/modemmanager-qt

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/modemmanager-qt-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-dev
BuildRequires:  ModemManager-dev >= 1.0.0

Requires:       kf5-filesystem

Obsoletes:      kf5-libmm-qt < 5.1.95
Provides:       kf5-libmm-qt%{?_isa} = %{version}-%{release}


%description
A Qt 5 library for ModemManager.

%package        dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-libmm-qt-dev < 5.1.95
Provides:       kf5-libmm-qt-dev = %{version}-%{release}
%description    dev
Qt 5 libraries and header files for developing applications
that use ModemManager.

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
%doc README README.md COPYING.LIB
%{_kf5_libdir}/libKF5ModemManagerQt.so.*

%files dev
%{_kf5_libdir}/libKF5ModemManagerQt.so
%{_kf5_libdir}/cmake/KF5ModemManagerQt
%{_kf5_includedir}/ModemManagerQt
%{_kf5_includedir}/modemmanagerqt_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_ModemManagerQt.pri

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
