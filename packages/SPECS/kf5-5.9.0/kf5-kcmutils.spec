%global framework kcmutils

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon with extra API to write KConfigModules

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
BuildRequires:  qt5-qtdeclarative-dev

BuildRequires:  kf5-kitemviews-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-kxmlgui-dev
BuildRequires:  kf5-kdeclarative-dev
BuildRequires:  kf5-kpackage-dev

Requires:       kf5-filesystem

%description
KCMUtils provides various classes to work with KCModules. KCModules can be
created with the KConfigWidgets framework.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfigwidgets-dev
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kitemviews-dev
Requires:       kf5-kservice-dev
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
%find_lang kcmutils5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kcmutils5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5KCMUtils.so.*
%{_kf5_datadir}/kservicetypes5/*.desktop

%files dev
%{_kf5_includedir}/kcmutils_version.h
%{_kf5_includedir}/KCMUtils
%{_kf5_libdir}/libKF5KCMUtils.so
%{_kf5_libdir}/cmake/KF5KCMUtils
%{_kf5_archdatadir}/mkspecs/modules/qt_KCMUtils.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
