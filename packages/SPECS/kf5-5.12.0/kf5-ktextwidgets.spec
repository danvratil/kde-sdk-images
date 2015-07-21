%global framework ktextwidgets

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon with advanced text editing widgets

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

BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-sonnet-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 addon with advanced text editing widgets.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcompletion-dev
Requires:       kf5-kconfigwidgets-dev
Requires:       kf5-ki18n-dev
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kservice-dev
Requires:       kf5-kwindowsystem-dev
Requires:       kf5-sonnet-dev
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
%find_lang ktextwidgets5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f ktextwidgets5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5TextWidgets.so.*
%{_kf5_datadir}/kservicetypes5/*.desktop

%files dev
%{_kf5_includedir}/ktextwidgets_version.h
%{_kf5_includedir}/KTextWidgets
%{_kf5_libdir}/libKF5TextWidgets.so
%{_kf5_libdir}/cmake/KF5TextWidgets
%{_kf5_archdatadir}/mkspecs/modules/qt_KTextWidgets.pri


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
