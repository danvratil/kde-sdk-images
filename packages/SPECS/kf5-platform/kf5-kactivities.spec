%global framework kactivities

%if 0%{?fedora} > 21
%global build_main_package 1
%endif

Name:           kf5-%{framework}
Summary:        A KDE Frameworks 5 Tier 3 to organize user work into separate activities
Version:        5.9.0
Release:        1%{?dist}

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

BuildRequires:  boost-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kglobalaccel-devel

BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kpackage-devel

Requires:       kf5-kactivities-libs%{?_isa} = %{version}-%{release}

Obsoletes:      kactivities < 4.90.0
Provides:       kactivities%{?_isa} = %{version}-%{release}
Provides:       kactivities = %{version}-%{release}

%description
A KDE Frameworks 5 Tier 3 API for using and interacting with Activities as a
consumer, application adding information to them or as an activity manager.

%package libs
Summary:        Libraries for KActivities framework
Requires:       kf5-filesystem
%description    libs
%{summary}.

%package devel
Summary:        Developer files for %{name}-libs
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
%description    devel
%{summary}.


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
%find_lang kactivities5_qt --with-qt --all-name

%if !0%{?build_main_package}
rm -f %{buildroot}%{_kf5_bindir}/kactivitymanagerd
rm -f %{buildroot}%{_kf5_datadir}/kservices5/*.desktop
rm -f %{buildroot}%{_kf5_datadir}/kservices5/*.protocol
rm -f %{buildroot}%{_kf5_datadir}/kservicetypes5/kactivitymanagerd-plugin.desktop
rm -rf %{buildroot}%{_kf5_qtplugindir}/kactivitymanagerd/
rm -r %{buildroot}%{_kf5_qtplugindir}/*.so
rm -rf %{buildroot}/%{_kf5_datadir}/kf5/kactivitymanagerd
%endif


%if 0%{?build_main_package}
%files
%doc README README.md README.packagers README.developers MAINTAINER
%{_kf5_bindir}/kactivitymanagerd
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/activities.protocol
%{_kf5_datadir}/kservicetypes5/kactivitymanagerd-plugin.desktop
%{_kf5_qtplugindir}/kactivitymanagerd/
%{_kf5_qtplugindir}/*.so
%{_kf5_datadir}/kf5/kactivitymanagerd/
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f kactivities5_qt.lang
%if !0%{?build_main_package}
%doc README README.md README.packagers README.developers MAINTAINER
%endif
%{_kf5_libdir}/libKF5Activities.so.*
%{_kf5_qmldir}/org/kde/activities/

%files devel
%{_kf5_libdir}/libKF5Activities.so
%{_kf5_libdir}/cmake/KF5Activities/
%{_kf5_includedir}/KActivities/
%{_kf5_includedir}/kactivities_version.h
%{_kf5_libdir}/pkgconfig/libKActivities.pc
%{_kf5_archdatadir}/mkspecs/modules/qt_KActivities.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
