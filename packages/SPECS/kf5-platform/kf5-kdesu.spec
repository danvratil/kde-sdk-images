%global framework kdesu

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 integration with su

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

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kpty-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 integration with su for elevated privileges.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kpty-devel

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
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kdesu5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kdesu5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5Su.so.*
%{_kf5_libexecdir}/kdesu_stub
%{_kf5_libexecdir}/kdesud

%files devel
%doc
%{_kf5_includedir}/kdesu_version.h
%{_kf5_includedir}/KDESu
%{_kf5_libdir}/libKF5Su.so
%{_kf5_libdir}/cmake/KF5Su
%{_kf5_archdatadir}/mkspecs/modules/qt_KDESu.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
