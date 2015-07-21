%global framework kemoticons

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 module with support for emoticons and emoticons themes

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
BuildRequires:  kf5-kcoreaddons-dev

BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kservice-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 module that provides emoticons themes as well as
helper classes to automatically convert text emoticons to graphical emoticons.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-karchive-dev
Requires:       kf5-kservice-dev
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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LIB README.md
%{_kf5_libdir}/libKF5Emoticons.so.*
%{_kf5_plugindir}/emoticonsthemes/*.so
%{_kf5_plugindir}/KEmoticonsIntegrationPlugin.so
%{_kf5_datadir}/kservices5/*
%{_kf5_datadir}/kservicetypes5/*
%{_kf5_datadir}/emoticons/Glass

%files dev
%{_kf5_includedir}/kemoticons_version.h
%{_kf5_includedir}/KEmoticons
%{_kf5_libdir}/libKF5Emoticons.so
%{_kf5_libdir}/cmake/KF5Emoticons
%{_kf5_archdatadir}/mkspecs/modules/qt_KEmoticons.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
