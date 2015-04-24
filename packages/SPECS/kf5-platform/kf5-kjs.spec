%global framework kjs

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 functional module with JavaScript interpret

License:        GPLv2+ and BSD
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/portingAids/%{framework}-%{version}.tar.xz

BuildRequires:  perl
BuildRequires:  pcre-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kdoctools-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 1 Tier 1 functional module with JavaScript interpret.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
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

chmod +x %{buildroot}/%{_kf5_datadir}/kf5/kjs/create_hash_table


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB README.md
%{_kf5_bindir}/kjs5
%{_kf5_libdir}/libKF5JS.so.*
%{_kf5_libdir}/libKF5JSApi.so.*
%{_kf5_datadir}/kf5/kjs/create_hash_table
%{_mandir}/man1/kjs5.1.gz

%files devel
%{_kf5_includedir}/kjs_version.h
%{_kf5_includedir}/kjs
%{_kf5_includedir}/wtf
%{_kf5_libdir}/libKF5JS.so
%{_kf5_libdir}/libKF5JSApi.so
%{_kf5_libdir}/cmake/KF5JS
%{_kf5_archdatadir}/mkspecs/modules/qt_KJS.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KJSApi.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
