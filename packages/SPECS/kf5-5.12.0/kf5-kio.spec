%global framework kio

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for filesystem abstraction

License:        GPLv2+ and MIT and BSD
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
BuildRequires:  qt5-qtx11extras-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-kwallet-dev
BuildRequires:  qt5-qtscript-dev
BuildRequires:  kf5-kxmlgui-dev
BuildRequires:  kf5-ktextwidgets-dev

BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kbookmarks-dev
BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kdbusaddons-dev
BuildRequires:  kf5-kdoctools-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kitemviews-dev
BuildRequires:  kf5-kjobwidgets-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-solid-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kwindowsystem-dev

Requires:       kf5-filesystem

Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-core-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-widgets = %{version}-%{release}
Requires:       %{name}-widgets-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-file-widgets%{?_isa} = %{version}-%{release}
Requires:       %{name}-ntlm%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 3 solution for filesystem abstraction

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kbookmarks-dev
Requires:       kf5-kcompletion-dev
Requires:       kf5-kconfig-dev
Requires:       kf5-kcoreaddons-dev
Requires:       kf5-kitemviews-dev
Requires:       kf5-kjobwidgets-dev
Requires:       kf5-kservice-dev
Requires:       kf5-solid-dev
Requires:       kf5-kxmlgui-dev
Requires:       qt5-qtbase-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    doc
Documentation for %{name}.

%package        core
Summary:        Core components of the KIO Framework
Requires:       %{name}-core-libs%{?_isa} = %{version}-%{release}
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    core
KIOCore library provides core non-GUI components for working with KIO.

%package        core-libs
Summary:        Runtime libraries for KIO Core
Requires:       %{name}-core = %{version}-%{release}
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    core-libs
%{summary}.

%package        widgets
Summary:        Widgets for KIO Framework
Requires:       %{name}-core%{?_isa} = %{version}-%{release}
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    widgets
KIOWidgets contains classes that provide generic job control, progress
reporting, etc.

%package        widgets-libs
Summary:        Runtime libraries for KIO Widgets library
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-widgets = %{version}-%{release}
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    widgets-libs
%{summary}.

%package        file-widgets
Summary:        Widgets for file-handling for KIO Framework
Requires:       %{name}-core%{?_isa} = %{version}-%{release}
Requires:       %{name}-widgets%{?_isa} = %{version}-%{release}
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    file-widgets
The KIOFileWidgets library provides the file selection dialog and
its components.

%package        ntlm
Summary:        NTLM support for KIO Framework
# last version of the main package before the split
Conflicts:      %{name} < 5.3.0-2
%description    ntlm
KIONTLM provides support for NTLM authentication mechanism in KIO


%prep
%setup -q -n %{framework}-%{version}

%build

# Yocto base SDK is missing the no-SOVERSION symlink,
# so we must compensate for that in order to make KIO
# compile.
#
# YES - we are actually making a symlink outside rpmbuild
# buildroot, but it does not matter, because the build env
# will be wiped anyway.
ln -s libcom_err.so.2 /lib/libcom_err.so


mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kio5 --with-qt --all-name

%files
%doc COPYING.LIB README.md

%post core
/usr/bin/update-desktop-database &> /dev/null || :
%postun core
/usr/bin/update-desktop-database &> /dev/null || :

%files core -f kio5.lang
%config %{_kf5_sysconfdir}/xdg/accept-languages.codes
%{_kf5_libexecdir}/kio_http_cache_cleaner
%{_kf5_libexecdir}/kpac_dhcp_helper
%{_kf5_libexecdir}/kioexec
%{_kf5_libexecdir}/kioslave
%{_kf5_libexecdir}/kiod5
%{_kf5_bindir}/ktelnetservice5
%{_kf5_bindir}/kcookiejar5
%{_kf5_bindir}/kmailservice5
%{_kf5_bindir}/ktrash5
%{_kf5_plugindir}/kio/*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_qtplugindir}/kcm_kio.so
%{_kf5_qtplugindir}/kcm_trash.so
%dir %{_kf5_plugindir}/kiod/
%{_kf5_plugindir}/kiod/*.so
%{_kf5_datadir}/kservices5/cache.desktop
%{_kf5_datadir}/kservices5/cookies.desktop
%{_kf5_datadir}/kservices5/netpref.desktop
%{_kf5_datadir}/kservices5/proxy.desktop
%{_kf5_datadir}/kservices5/smb.desktop
%{_kf5_datadir}/kservices5/useragent.desktop
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/http_cache_cleaner.desktop
%dir %{_kf5_datadir}/kservices5/kded/
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservices5/kcmtrash.desktop
%{_kf5_datadir}/kservices5/useragentstrings
%{_kf5_datadir}/knotifications5/proxyscout.*
%{_kf5_datadir}/kf5/kcookiejar/domain_info
%{_kf5_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.kde.kiod5.service

%post core-libs -p /sbin/ldconfig
%postun core-libs -p /sbin/ldconfig

%files core-libs
%{_kf5_libdir}/libKF5KIOCore.so.*

%post widgets
/usr/bin/update-desktop-database &> /dev/null || :
%postun widgets
/usr/bin/update-desktop-database &> /dev/null || :

%files widgets
%config %{_kf5_sysconfdir}/xdg/kshorturifilterrc
%{_kf5_qtplugindir}/kcm_webshortcuts.so
%{_kf5_plugindir}/urifilters/*.so
%{_kf5_datadir}/kservices5/fixhosturifilter.desktop
%{_kf5_datadir}/kservices5/kshorturifilter.desktop
%{_kf5_datadir}/kservices5/kuriikwsfilter.desktop
%{_kf5_datadir}/kservices5/kurisearchfilter.desktop
%{_kf5_datadir}/kservices5/localdomainurifilter.desktop
%{_kf5_datadir}/kservices5/webshortcuts.desktop
%{_kf5_datadir}/kservices5/searchproviders
%{_kf5_datadir}/kservicetypes5/*.desktop

%post widgets-libs -p /sbin/ldconfig
%postun widgets-libs -p /sbin/ldconfig

%files widgets-libs
%{_kf5_libdir}/libKF5KIOWidgets.so.*

%post file-widgets -p /sbin/ldconfig
%postun file-widgets -p /sbin/ldconfig

%files file-widgets
%{_kf5_libdir}/libKF5KIOFileWidgets.so.*

%post ntlm -p /sbin/ldconfig
%postun ntlm -p /sbin/ldconfig

%files ntlm
%{_kf5_libdir}/libKF5KIONTLM.so.*

%files dev
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5KIO
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOFileWidgets.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KNTLM.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOWidgets.pri
%{_datadir}/dbus-1/interfaces/*.xml

%files doc
%{_kf5_mandir}/man8/*
%{_kf5_mandir}/*/man8/*
%exclude %{_kf5_mandir}/man8
%{_kf5_datadir}/doc/HTML/en/kioslave5/


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
