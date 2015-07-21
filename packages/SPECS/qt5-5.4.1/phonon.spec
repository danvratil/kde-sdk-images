Summary: Multimedia framework api
Name:    phonon
Version: 4.8.3
Release: 1%{?dist}
License: LGPLv2+
URL:     http://phonon.kde.org/

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/phonon/%{version}/src/phonon-%{version}.tar.xz

Patch0: phonon-4.7.0-rpath_use_link_path.patch

BuildRequires: qt5-sdk-base

BuildRequires: glib2-dev
BuildRequires: libxcb-dev

BuildRequires: qt5-qtbase-dev
BuildRequires: qt5-qtquick1-dev
BuildRequires: qt5-qttools-dev
BuildRequires: qt5-qttools-static

BuildRequires: pulseaudio-libs-dev

%global pulseaudio_version %((pkg-config --modversion libpulse 2>/dev/null || echo 0.9.15) | cut -d- -f1)

Provides: phonon-backend%{?_isa} = 4.7
Requires: pulseaudio-libs%{?_isa} >= %{pulseaudio_version}

%description
%{summary}.

%package dev
Summary: Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description dev
%{summary}.

%prep
%setup -q

%patch0 -p1 -b .rpath_use_link_path

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DPHONON_BUILD_PHONON4QT5:BOOL=ON \
  -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

mkdir -p %{buildroot}%{_qt5_plugindir}/phonon4qt5_backend

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB
%dir %{_datadir}/phonon4qt5
%{_libdir}/libphonon4qt5.so.4*
%{_libdir}/libphonon4qt5experimental.so.4*
%{_qt5_plugindir}/designer/libphononwidgets.so
%dir %{_qt5_plugindir}/phonon4qt5_backend/
%{_datadir}/dbus-1/interfaces/org.kde.Phonon4Qt5.AudioOutput.xml

%files dev
%{_datadir}/phonon4qt5/buildsystem/
%dir %{_libdir}/cmake/
%{_libdir}/cmake/phonon4qt5/
%{_includedir}/phonon4qt5/
%{_libdir}/libphonon4qt5.so
%{_libdir}/libphonon4qt5experimental.so
%{_libdir}/pkgconfig/phonon4qt5.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_phonon4qt5.pri

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 4.8.3-1
- Initial version (forked from Fedora, removed Qt 4 build)
