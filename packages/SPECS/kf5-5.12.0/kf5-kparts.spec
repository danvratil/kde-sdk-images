%global framework kparts

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for KParts

License:        GPLv2+
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
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-kjobwidgets-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-ktextwidgets-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kxmlgui-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for KParts

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kio-dev
Requires:       kf5-knotifications-dev
Requires:       kf5-ktextwidgets-dev
Requires:       kf5-kxmlgui-dev

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
%find_lang kparts5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kparts5_qt.lang
%doc COPYING.LIB README.md AUTHORS
%{_kf5_libdir}/libKF5Parts.so.*
%{_kf5_datadir}/kservicetypes5/*.desktop

%files dev
%{_kf5_includedir}/kparts_version.h
%{_kf5_includedir}/KParts
%{_kf5_libdir}/libKF5Parts.so
%{_kf5_libdir}/cmake/KF5Parts
%{_kf5_archdatadir}/mkspecs/modules/qt_KParts.pri


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
