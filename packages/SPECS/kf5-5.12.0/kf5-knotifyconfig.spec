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
BuildRequires:  phonon-dev
BuildRequires:  qt5-qtbase-dev
BuildRequires:  kf5-kxmlgui-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kconfigwidgets-dev

BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-kservice-dev

Requires:       kf5-filesystem

%description
%{summary}.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ki18n-dev
Requires:       kf5-kio-dev
Requires:       qt5-qtbase-dev

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
%find_lang knotifyconfig5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f knotifyconfig5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5NotifyConfig.so.*

%files dev
%{_kf5_includedir}/knotifyconfig_version.h
%{_kf5_includedir}/KNotifyConfig
%{_kf5_libdir}/libKF5NotifyConfig.so
%{_kf5_libdir}/cmake/KF5NotifyConfig
%{_kf5_archdatadir}/mkspecs/modules/qt_KNotifyConfig.pri


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
