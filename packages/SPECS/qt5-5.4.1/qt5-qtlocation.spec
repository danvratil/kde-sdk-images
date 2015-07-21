%global qt_module qtlocation

Summary: Qt5 - Location component
Name:    qt5-%{qt_module}%{?bootstrap:-bootstrap}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base

BuildRequires: qt5-qtbase%{?bootstrap:-bootstrap}-dev
BuildRequires: qt5-qtdeclarative%{?bootstrap:-bootstrap}-dev

# TODO
#BuildRequires: pkgconfig(geoclue)
#BuildRequires: pkgconfig(gypsy)

%{?_qt5_version:Requires: qt5-qtbase%{?bootstrap:-bootstrap}%{?_isa} >= %{_qt5_version}}

%description
The Qt Location and Qt Positioning APIs gives developers the ability to
determine a position by using a variety of possible sources, including
satellite, or wifi, or text file, and so on.

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase%{?bootstrap:-bootstrap}-dev%{?_isa}
%description dev
%{summary}.

%if ! 0%{?bootstrap}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if ! 0%{?bootstrap}
make %{?_smp_mflags} docs
%endif
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if ! 0%{?bootstrap}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt5Location.so.5*
%{_qt5_archdatadir}/qml/QtLocation/
%{_qt5_plugindir}/geoservices/
%{_qt5_libdir}/libQt5Positioning.so.5*
%{_qt5_archdatadir}/qml/QtPositioning/
%{_qt5_plugindir}/position/
%dir %{_qt5_libdir}/cmake/
%dir %{_qt5_libdir}/cmake/Qt5Location
%dir %{_qt5_libdir}/cmake/Qt5Positioning
%{_qt5_libdir}/cmake/Qt5Location/Qt5Location_QGeoServiceProviderFactory*.cmake
%{_qt5_libdir}/cmake/Qt5Positioning/Qt5Positioning_QGeoPositionInfoSourceFactory*.cmake

%files dev
%{_qt5_headerdir}/QtLocation/
%{_qt5_libdir}/libQt5Location.so
%{_qt5_libdir}/libQt5Location.prl
%{_qt5_libdir}/pkgconfig/Qt5Location.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_location*.pri
%{_qt5_libdir}/cmake/Qt5Location/Qt5LocationConfig*.cmake
%{_qt5_headerdir}/QtPositioning/
%{_qt5_libdir}/libQt5Positioning.so
%{_qt5_libdir}/libQt5Positioning.prl
%{_qt5_libdir}/cmake/Qt5Positioning/Qt5PositioningConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Positioning.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri

%if ! 0%{?bootstrap}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtlocation.qch
%{_qt5_docdir}/qtlocation/
%{_qt5_docdir}/qtpositioning.qch
%{_qt5_docdir}/qtpositioning/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
