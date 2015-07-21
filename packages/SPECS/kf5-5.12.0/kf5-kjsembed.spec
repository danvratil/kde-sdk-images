%global framework kjsembed

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon for binding JS objects to QObjects

License:        LGPLv2+
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/portingAids/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtsvg-dev

BuildRequires:  kf5-kjs-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kdoctools-dev

Requires:       kf5-filesystem

%description
KSJEmbed provides a method of binding JavaScript objects to QObjects, so you
can script your applications.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kjs-dev
Requires:       kf5-ki18n-dev

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
%find_lang kjsembed5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kjsembed5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/kjscmd5
%{_kf5_bindir}/kjsconsole
%{_kf5_libdir}/libKF5JsEmbed.so.*
%{_kf5_datadir}/man/man1/*

%files dev
%{_kf5_libdir}/libKF5JsEmbed.so
%{_kf5_libdir}/cmake/KF5JsEmbed
%{_kf5_includedir}/KJsEmbed/
%{_kf5_archdatadir}/mkspecs/modules/qt_KJsEmbed.pri


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
