%global framework ki18n

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon for localization

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
BuildRequires:  qt5-qtscript-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 1 addon for localization.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{framework}-%{version} -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang ki18n5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f ki18n5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5I18n.so.*
%{_kf5_qtplugindir}/kf5/ktranscript.so
%{_datadir}/locale/*/LC_SCRIPTS/ki18n5/ki18n5.js
# Trapnakron files are too large to be installed by default
%lang(sr) %{_datadir}/locale/sr/LC_SCRIPTS/ki18n5/trapnakron.pmap
%lang(sr) %{_datadir}/locale/sr/LC_SCRIPTS/ki18n5/trapnakron.pmapc
%lang(sr@ijekavian) %{_datadir}/locale/sr@ijekavian/LC_SCRIPTS/ki18n5/trapnakron.pmap
%lang(sr@ijekavian) %{_datadir}/locale/sr@ijekavian/LC_SCRIPTS/ki18n5/trapnakron.pmapc
%lang(sr@ijekavianlatin) %{_datadir}/locale/sr@ijekavianlatin/LC_SCRIPTS/ki18n5/trapnakron.pmap
%lang(sr@ijekavianlatin) %{_datadir}/locale/sr@ijekavianlatin/LC_SCRIPTS/ki18n5/trapnakron.pmapc
%lang(sr@latin) %{_datadir}/locale/sr@latin/LC_SCRIPTS/ki18n5/trapnakron.pmap
%lang(sr@latin) %{_datadir}/locale/sr@latin/LC_SCRIPTS/ki18n5/trapnakron.pmapc
%lang(fi) %{_datadir}/locale/fi/LC_SCRIPTS/ki18n5/general.pmap
%lang(fi) %{_datadir}/locale/fi/LC_SCRIPTS/ki18n5/general.pmapc

%files dev
%{_kf5_includedir}/ki18n_version.h
%{_kf5_includedir}/KI18n
%{_kf5_libdir}/libKF5I18n.so
%{_kf5_libdir}/cmake/KF5I18n
%{_kf5_archdatadir}/mkspecs/modules/qt_KI18n.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
