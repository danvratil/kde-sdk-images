%global snapshot 20140604
%global tarballversion 0.9.2

Summary:        A Qt implementation of the DBusMenu protocol (Qt5 version)
Name:           dbusmenu-qt5
Version:        0.9.3
Release:        0.3.%{snapshot}bzr%{?dist}

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://launchpad.net/libdbusmenu-qt/

#Source0 :       https://launchpad.net/libdbusmenu-qt/trunk/%{version}/+download/libdbusmenu-qt-%{version}.tar.bz2
# bzr branch lp:libdbusmenu-qt && mv libdbusmenu-qt{,5-%{version}} && \
# tar -c libdbusmenu-qt5-0.9.2 | bzip2 -c > libdbusmenu-qt5-0.9.2-${snapshot}bzr.tar.bz2
# Last upstream release does not include Qt5 support, so we need to use a snapshot
Source0:        libdbusmenu-qt5-%{version}-%{snapshot}bzr.tar.bz2

BuildRequires:  qt5-sdk-base
BuildRequires:  qt5-qtbase-devel

%description
This library provides a Qt implementation of the DBusMenu protocol.

The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.


%package        dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    dev
%{summary}.


%prep
%setup -q -n libdbusmenu-qt5-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
        -DUSE_QT4:BOOL=FALSE \
        -DUSE_QT5:BOOL=TRUE \
        -DWITH_DOC:BOOL=TRUE \
        ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
rm -rf %{buildroot}%{_docdir}/dbusmenu-qt


%check
# verify pkg-config version
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion dbusmenu-qt5)" = "%{tarballversion}"
# test suite
xvfb-run dbus-launch make -C %{_target_platform} check ||:


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libdbusmenu-qt5.so.2*
%{_datadir}/doc/libdbusmenu-qt5-doc/

%files dev
%defattr(-,root,root,-)
%{_includedir}/dbusmenu-qt5/
%{_libdir}/libdbusmenu-qt5.so
%{_libdir}/pkgconfig/dbusmenu-qt5.pc
%{_libdir}/cmake/dbusmenu-qt5/


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.3-0.3.20140604bzr
- Intial version (forked from Fedora)
