%global framework kwidgetsaddons

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon with various classes on top of QtWidgets

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

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qttools-dev
BuildRequires:  qt5-qttools-static

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 1 addon with various classes on top of QtWidgets.


%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
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
%make_install -C %{_target_platform}
%find_lang kwidgetsaddons5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kwidgetsaddons5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5WidgetsAddons.so.*
%{_kf5_datadir}/kf5/kcharselect

%files dev
%{_kf5_includedir}/kwidgetsaddons_version.h
%{_kf5_includedir}/KWidgetsAddons
%{_kf5_libdir}/libKF5WidgetsAddons.so
%{_kf5_libdir}/cmake/KF5WidgetsAddons
%{_kf5_archdatadir}/mkspecs/modules/qt_KWidgetsAddons.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
