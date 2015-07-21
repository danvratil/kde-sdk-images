%global framework attica

Name:           kf5-attica
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks Tier 1 Addon with Open Collaboration Services API

Group:          Development/Libraries
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

Requires:       kf5-filesystem

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.4.

%package        dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-dev

%description    dev
%{summary}.


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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README.md
%doc ChangeLog
%{_kf5_libdir}/libKF5Attica.so.*

%files dev
%{_kf5_libdir}/cmake/KF5Attica/
%{_kf5_includedir}/attica_version.h
%{_kf5_includedir}/Attica/
%{_kf5_libdir}/libKF5Attica.so
%{_kf5_archdatadir}/mkspecs/modules/qt_Attica.pri
%{_kf5_libdir}/pkgconfig/libKF5Attica.pc


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
