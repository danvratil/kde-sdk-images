%global framework kross

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for multi-language application scripting

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
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qttools-static

BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kxmlgui-devel

Requires:       %{name}-core%{_isa} = %{version}-%{release}
Requires:       %{name}-ui%{?_isa} = %{version}-%{release}

%description
Kross is a scripting bridge to embed scripting functionality into an
application. It supports QtScript as a scripting interpreter backend.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ki18n-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-kio-devel
Requires:       kf5-kparts-devel
Requires:       kf5-kwidgetsaddons-devel
Requires:       qt5-qtbase-devel
Requires:       qt5-qtscript-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        core
Summary:        Non-gui part of the Kross framework
Requires:       kf5-filesystem
%description    core
Non-gui part of the Kross framework.

%package        ui
Summary:        Gui part of the Kross framework
Requires:       %{name}-core%{?_isa} = %{version}-%{release}
Requires:       kf5-filesystem
%description    ui
Gui part of the Kross framework.

%package        doc
Summary:        Documentation and user manuals for the Kross framework
%description    doc
Documentation and user manuals for the Kross framework


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
%find_lang kross5_qt --with-qt --all-name


%files

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%files core -f kross5_qt.lang
%{_kf5_bindir}/kf5kross
%{_kf5_libdir}/libKF5KrossCore.so.*
%{_kf5_qtplugindir}/krossqts.so
%{_kf5_qtplugindir}/script/krossqtsplugin.so

%post ui -p /sbin/ldconfig
%postun ui -p /sbin/ldconfig

%files ui
%{_kf5_libdir}/libKF5KrossUi.so.*
%{_kf5_qtplugindir}/KrossModuleForms.so
%{_kf5_qtplugindir}/KrossModuleKdeTranslation.so

%files doc
%doc COPYING.LIB README.md
%{_kf5_datadir}/man/man1/*

%files devel
%{_kf5_includedir}/kross_version.h
%{_kf5_includedir}/KrossUi
%{_kf5_includedir}/KrossCore
%{_kf5_libdir}/libKF5KrossCore.so
%{_kf5_libdir}/libKF5KrossUi.so
%{_kf5_libdir}/cmake/KF5Kross
%{_kf5_archdatadir}/mkspecs/modules/qt_KrossCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KrossUi.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
