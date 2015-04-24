%global framework plasma

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 framework is foundation to build a primary user interface

License:        GPLv2+ and LGPLv2+ and BSD
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-framework-%{version}.tar.xz

BuildRequires:  libX11-dev
BuildRequires:  libxcb-dev
BuildRequires:  libXrender-dev
BuildRequires:  libXScrnSaver-dev
BuildRequires:  libXext-dev
BuildRequires:  libSM-dev
BuildRequires:  libGL-dev

BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtx11extras-dev
BuildRequires:  qt5-qtdeclarative-dev
BuildRequires:  qt5-qtsvg-dev
BuildRequires:  qt5-qtscript-dev

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kactivities-dev
BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kdbusaddons-dev
BuildRequires:  kf5-kdeclarative-dev
BuildRequires:  kf5-kglobalaccel-dev
BuildRequires:  kf5-kguiaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-kxmlgui-dev
BuildRequires:  kf5-kdoctools-dev
BuildRequires:  kf5-kpackage-dev
BuildRequires:  kf5-kdesu-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-solid-dev
BuildRequires:  kf5-kparts-dev
BuildRequires:  kf5-kconfig-dev

Requires:       kf5-filesystem

%description
%{summary}.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       extra-cmake-modules
Requires:       kf5-kpackage-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-framework-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang plasma5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f plasma5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/plasmapkg2
%{_kf5_libdir}/libKF5Plasma.so.*
%{_kf5_libdir}/libKF5PlasmaQuick.so.*
%{_kf5_qmldir}/org/kde/*
%{_kf5_qmldir}/QtQuick/Controls/Styles/Plasma
%{_kf5_qtplugindir}/*.so
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/plasma/
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_mandir}/man1/plasmapkg2.1.gz
%{_kf5_plugindir}/kded/platformstatus.so

%lang(lt) %{_datadir}/locale/lt/LC_SCRIPTS/libplasma5/*.js

%files dev
%{_kf5_libdir}/cmake/KF5Plasma
%{_kf5_libdir}/cmake/KF5PlasmaQuick
%{_kf5_libdir}/libKF5Plasma.so
%{_kf5_libdir}/libKF5PlasmaQuick.so
%{_kf5_includedir}/plasma_version.h
%{_kf5_includedir}/plasma/
%{_kf5_includedir}/Plasma/


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
