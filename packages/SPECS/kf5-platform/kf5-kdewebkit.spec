%global framework kdewebkit

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 integration module for QtWebKit

License:        LGPLv2+
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
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwallet-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 integration module for the HTML rendering engine WebKit.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtwebkit-devel

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
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5WebKit.so.*

%files devel
%{_kf5_includedir}/kdewebkit_version.h
%{_kf5_includedir}/KDEWebKit
%{_kf5_libdir}/libKF5WebKit.so
%{_kf5_libdir}/cmake/KF5WebKit
%{_kf5_archdatadir}/mkspecs/modules/qt_KDEWebKit.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
