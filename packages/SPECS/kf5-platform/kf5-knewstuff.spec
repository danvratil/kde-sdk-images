%global framework knewstuff

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 module for downloading application assets

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
BuildRequires:  kf5-attica-dev

BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-kitemviews-dev
BuildRequires:  kf5-ktextwidgets-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kxmlgui-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 module for downloading and sharing additional
application data like plugins, themes, motives, etc.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-attica-dev
Requires:       kf5-karchive-dev
Requires:       kf5-kio-dev
Requires:       kf5-kxmlgui-dev
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
%find_lang knewstuff5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f knewstuff5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5NewStuff.so.*
%{_kf5_datadir}/kf5/knewstuff/

%files dev
%{_kf5_includedir}/knewstuff_version.h
%{_kf5_includedir}/KNewStuff3
%{_kf5_libdir}/libKF5NewStuff.so
%{_kf5_libdir}/cmake/KF5NewStuff
%{_kf5_archdatadir}/mkspecs/modules/qt_KNewStuff.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
