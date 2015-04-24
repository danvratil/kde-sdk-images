%global framework frameworkintegration

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 workspace and cross-framework integration plugins
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

# upstream patches
Patch0:         frameworkintegration-5.9-fix-native-dialogs.patch

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtx11extras-dev

BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kwidgetsaddons-dev
#BuildRequires:  oxygen-fonts-dev

BuildRequires:  libXcursor-dev

Requires:       kf5-filesystem
#Requires:       oxygen-fonts

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
Framework Integration is a set of plugins responsible for better integration of
Qt applications when running on a KDE Plasma workspace.

Applications do not need to link to this directly.

%package        libs
Summary:        Runtime libraries for %{name}.
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    libs
%{summary}.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kconfigwidgets-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang frameworkintegration5_qt --with-qt --all-name


%files -f frameworkintegration5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_datadir}/kf5/infopage/*
%{_kf5_datadir}/knotifications5/plasma_workspace.notifyrc
%{_kf5_plugindir}/FrameworkIntegrationPlugin.so
%{_kf5_qtplugindir}/platformthemes/KDEPlatformTheme.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libKF5Style.so.*

%files dev
%{_kf5_includedir}/frameworkintegration_version.h
%{_kf5_includedir}/KStyle
%{_kf5_libdir}/libKF5Style.so
%{_kf5_libdir}/cmake/KF5FrameworkIntegration


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
