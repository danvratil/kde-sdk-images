%global framework kwallet

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for password management

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
BuildRequires:  qt5-qtbase-dev

BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kdbusaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-kwidgetsaddons-dev

Obsoletes:      kf5-kwallet-runtime < 5.8.0-2
Provides:       kf5-kwallet-runtime = %{version}-%{release}
Provides:       kf5-kwallet-runtime%{?_isa} = %{version}-%{release}

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
KWallet is a secure and unified container for user passwords.

%package        libs
Summary:        KWallet framework libraries
Requires:       kf5-filesystem
Requires:       %{name} = %{version}-%{release}
%description    libs
Provides API to access KWallet data from applications.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-dev
Requires:       kf5-kwindowsystem-dev
Requires:       qt5-qtbase-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang %{name} --with-qt --all-name


%files -f %{name}.lang
%doc COPYING.LIB README.md
%{_kf5_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_kf5_datadir}/dbus-1/services/org.kde.kwalletd.service
%{_kf5_bindir}/kwalletd5
%{_kf5_datadir}/kservices5/kwalletd5.desktop
%{_kf5_datadir}/knotifications5/kwalletd.notifyrc

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libKF5Wallet.so.*
%{_kf5_libdir}/libkwalletbackend5.so.*

%files dev
%{_kf5_datadir}/dbus-1/interfaces/kf5_org.kde.KWallet.xml
%{_kf5_includedir}/kwallet_version.h
%{_kf5_includedir}/KWallet
%{_kf5_libdir}/cmake/KF5Wallet
%{_kf5_libdir}/libKF5Wallet.so
%{_kf5_libdir}/libkwalletbackend5.so
%{_kf5_archdatadir}/mkspecs/modules/qt_KWallet.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
