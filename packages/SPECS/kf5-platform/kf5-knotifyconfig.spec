%global framework knotifyconfig

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 module for KNotify configuration

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
BuildRequires:  phonon-qt5-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kconfigwidgets-devel

BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kservice-devel

Requires:       kf5-filesystem

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ki18n-devel
Requires:       kf5-kio-devel
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
%find_lang knotifyconfig5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f knotifyconfig5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5NotifyConfig.so.*

%files devel
%{_kf5_includedir}/knotifyconfig_version.h
%{_kf5_includedir}/KNotifyConfig
%{_kf5_libdir}/libKF5NotifyConfig.so
%{_kf5_libdir}/cmake/KF5NotifyConfig
%{_kf5_archdatadir}/mkspecs/modules/qt_KNotifyConfig.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
