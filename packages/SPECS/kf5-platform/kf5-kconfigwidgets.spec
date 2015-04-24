%global framework kconfigwidgets

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon for creating configuration dialogs

License:        GPLv2+ and LGPLv2+ and MIT
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

BuildRequires:  kf5-kauth-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kcodecs-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kdoctools-dev
BuildRequires:  kf5-kguiaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kwidgetsaddons-dev

Requires:       kf5-filesystem

%description
KConfigWidgets provides easy-to-use classes to create configuration dialogs, as
well as a set of widgets which uses KConfig to store their settings.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kauth-dev
Requires:       kf5-kcodecs-dev
Requires:       kf5-kconfig-dev
Requires:       kf5-kguiaddons-dev
Requires:       kf5-ki18n-dev
Requires:       kf5-kwidgetsaddons-dev

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
%find_lang kconfigwidgets5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kconfigwidgets5_qt.lang
%doc COPYING COPYING.LIB README.md
%{_kf5_libdir}/libKF5ConfigWidgets.so.*
%{_kf5_bindir}/preparetips5
%{_kf5_datadir}/kf5/kconfigwidgets
%{_kf5_mandir}/man1/*
%{_kf5_datadir}/locale/*/kf5_entry.desktop

%files dev
%{_kf5_includedir}/kconfigwidgets_version.h
%{_kf5_includedir}/KConfigWidgets
%{_kf5_libdir}/libKF5ConfigWidgets.so
%{_kf5_libdir}/cmake/KF5ConfigWidgets
%{_kf5_archdatadir}/mkspecs/modules/qt_KConfigWidgets.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
