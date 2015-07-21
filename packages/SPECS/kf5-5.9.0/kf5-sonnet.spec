%global framework sonnet

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 solution for spell checking

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

BuildRequires:  libupnp-dev
#BuildRequires:  systemd-dev
BuildRequires:  hunspell-dev

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qttools-dev

Requires:       kf5-filesystem
Requires:       kf5-sonnet-core%{?_isa} = %{version}-%{release}
Requires:       kf5-sonnet-ui%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 1 solution for spell checking.


%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%package        core
Summary:        Non-gui part of the Sonnet framework

%description    core
Non-gui part of the Sonnet framework provides low-level spell checking tools

%package        ui
Summary:        GUI part of the Sonnet framework
Requires:       kf5-sonnet-core%{?_isa} = %{version}-%{release}

%description    ui
GUI part of the Sonnet framework provides widgets with spell checking support.


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
%find_lang sonnet5_qt --with-qt --all-name


%files
%doc COPYING.LIB README.md

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%files core
%{_kf5_libdir}/libKF5SonnetCore.so.*
%{_kf5_plugindir}/sonnet
%{_kf5_datadir}/kf5/sonnet/trigrams.map

%post ui -p /sbin/ldconfig
%postun ui -p /sbin/ldconfig

%files ui -f sonnet5_qt.lang
%{_kf5_libdir}/libKF5SonnetUi.so.*

%files dev
%{_kf5_includedir}/sonnet_version.h
%{_kf5_includedir}/SonnetCore
%{_kf5_includedir}/SonnetUi
%{_kf5_libdir}/libKF5SonnetCore.so
%{_kf5_libdir}/libKF5SonnetUi.so
%{_kf5_libdir}/cmake/KF5Sonnet
%{_kf5_archdatadir}/mkspecs/modules/qt_SonnetCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_SonnetUi.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
