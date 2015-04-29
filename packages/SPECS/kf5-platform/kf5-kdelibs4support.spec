%global framework kdelibs4support

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 module with porting aid from KDELibs 4
License:        GPLv2+ and LGPLv2+ and BSD
URL:            https://projects.kde.org/projects/frameworks/kdelibs4support

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/portingAids/%{framework}-%{version}.tar.xz

BuildRequires:  libX11-dev
BuildRequires:  libSM-dev

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtsvg-dev
BuildRequires:  qt5-qtx11extras-dev
BuildRequires:  qt5-qttools-dev

BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-kcrash-dev
BuildRequires:  kf5-kdesignerplugin-dev
BuildRequires:  kf5-kglobalaccel-dev
BuildRequires:  kf5-kdoctools-dev
BuildRequires:  kf5-kguiaddons-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kparts-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-ktextwidgets-dev
BuildRequires:  kf5-kunitconversion-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-kxmlgui-dev

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
#Requires:       ca-certificates
#Requires:       kde-settings
Requires:       kf5-filesystem

%description
This framework provides code and utilities to ease the transition from kdelibs 4
to KDE Frameworks 5. This includes CMake macros and C++ classes whose
functionality has been replaced by code in CMake, Qt and other frameworks.

%package        libs
Summary:        Runtime libraries for %{name}
Requires:       %{name} = %{version}-%{release}
# When the split occured
Conflicts:      %{name} < 5.4.0-1
%description    libs
%{summary}.

%package        doc
Summary:        Documentation and user manuals for %{name}
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 5.4.0-1
BuildArch:      noarch
%description    doc
%{summary}.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kauth-dev
Requires:       kf5-kconfigwidgets-dev
Requires:       kf5-kcoreaddons-dev
Requires:       kf5-kcrash-dev
Requires:       kf5-kdesignerplugin-dev
Requires:       kf5-kdoctools-dev
Requires:       kf5-kemoticons-dev
Requires:       kf5-kguiaddons-dev
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kinit-dev
Requires:       kf5-kitemmodels-dev
Requires:       kf5-knotifications-dev
Requires:       kf5-kparts-dev
Requires:       kf5-ktextwidgets-dev
Requires:       kf5-kunitconversion-dev
Requires:       kf5-kwindowsystem-dev
Requires:       qt5-qtbase-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}


%build
# Get rid of Perl dependencies. It's impossible to get it work
# in this lousy runtime
echo -e "function(kdelibs4support_encode_uri _original_uri)\nendfunction()" > cmake/uriencode.cmake

mkdir %{_target_platform}
pushd %{_target_platform}
# Set absolute BIN_INSTALL_DIR, otherwise CMake will complain about mixed use of
# absolute and relative paths for some reason
# Remove once fixed upstream
%{cmake_kf5} .. \
        -DBIN_INSTALL_DIR=%{_kf5_bindir}
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kdelibs4support5_qt --with-qt --all-name

## use ca-certificates' ca-bundle.crt, symlink as what most other
## distros do these days (http://bugzilla.redhat.com/521902)
if [  -f %{buildroot}%{_kf5_datadir}/kf5/kssl/ca-bundle.crt -a \
      -f /etc/pki/tls/certs/ca-bundle.crt ]; then
  ln -sf /etc/pki/tls/certs/ca-bundle.crt \
         %{buildroot}%{_kf5_datadir}/kf5/kssl/ca-bundle.crt
fi

## use kdebugrc from kde-settings instead
rm -fv %{buildroot}%{_kf5_sysconfdir}/xdg/kdebugrc


%files -f kdelibs4support5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/kf5-config
%{_kf5_bindir}/kdebugdialog5
%{_kf5_libexecdir}/fileshareset
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/qimageioplugins/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/kservices5/kded/networkstatus.desktop
%{_kf5_datadir}/kf5/kdoctools/customization
%{_kf5_datadir}/kf5/locale/*
%{_kf5_datadir}/locale/kf5_all_languages
%{_kf5_datadir}/kf5/widgets/
%{_kf5_datadir}/kf5/kssl/ca-bundle.crt
%config %{_kf5_sysconfdir}/xdg/colors
%config %{_kf5_sysconfdir}/xdg/kdebug.areas
# not sure how this is used exactly yet -- rex
%config %{_kf5_sysconfdir}/xdg/ksslcalist

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libKF5KDELibs4Support.so.*
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/designer/*.so
%{_kf5_plugindir}/kio/metainfo.so
%{_kf5_plugindir}/kded/networkstatus.so

%files doc
%{_kf5_docdir}/HTML/*/kdebugdialog5
%{_kf5_mandir}/man1/*
%{_kf5_mandir}/*/man1/*
%exclude %{_kf5_mandir}/man1

%files dev
%{_kf5_libdir}/libKF5KDELibs4Support.so
%{_kf5_libdir}/cmake/KF5KDELibs4Support/
%{_kf5_libdir}/cmake/KF5KDE4Support/
%{_kf5_libdir}/cmake/KDELibs4/
%{_kf5_includedir}/kdelibs4support_version.h
%{_kf5_includedir}/KDELibs4Support/
%{_kf5_datadir}/dbus-1/interfaces/*.xml


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
