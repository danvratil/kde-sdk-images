%global framework khtml

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 solution with KHTML, a HTML rendering engine

License:        LGPLv2+ and GPLv3 and MIT and BSD
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/portingAids/%{framework}-%{version}.tar.xz

BuildRequires:  fdupes
BuildRequires:  giflib-dev

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtx11extras-dev
BuildRequires:  phonon-qt5-dev

BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kcodecs-dev
BuildRequires:  kf5-kglobalaccel-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-kjs-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kparts-dev
BuildRequires:  kf5-ktextwidgets-dev
BuildRequires:  kf5-kwallet-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-kxmlgui-dev
BuildRequires:  kf5-sonnet-dev

Requires:       kf5-filesystem

%description
KHTML is a web rendering engine, based on the KParts technology and using KJS
for JavaScript support.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-karchive-dev
Requires:       kf5-kbookmarks-dev
Requires:       kf5-kglobalaccel-dev
Requires:       kf5-ki18n-dev
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kio-dev
Requires:       kf5-kjs-dev
Requires:       kf5-knotifications-dev
Requires:       kf5-kparts-dev
Requires:       kf5-kwallet-dev
Requires:       kf5-kwidgetsaddons-dev
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
%{cmake_kf5} .. -DCMAKE_SHARED_LINKER_FLAGS="-Wl,--as-needed"
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang khtml5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f khtml5_qt.lang
%doc COPYING.GPL3 COPYING.LIB README.md
%{_kf5_libdir}/libKF5KHtml.so.*
%{_kf5_plugindir}/parts/*.so
%{_kf5_datadir}/kf5/kjava/
%{_kf5_datadir}/kf5/khtml/
%{_kf5_datadir}/kxmlgui5/khtml/
%{_kf5_datadir}/kservices5/*.desktop
%config %{_kf5_sysconfdir}/xdg/khtmlrc

%files dev
%doc
%{_kf5_libdir}/libKF5KHtml.so
%{_kf5_libdir}/cmake/KF5KHtml
%{_kf5_includedir}/KHtml/
%{_kf5_includedir}/khtml_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_KHtml.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
