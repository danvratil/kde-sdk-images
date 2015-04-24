%global qt_module qtsvg

Summary: Qt5 - Support for rendering and displaying SVG
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: qt5-qtbase-dev

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
Scalable Vector Graphics (SVG) is an XML-based language for describing
two-dimensional vector graphics. Qt provides classes for rendering and
displaying SVG drawings in widgets and on other paint devices.

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-dev%{?_isa}
%description dev
%{summary}.

%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.

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
make %{?_smp_mflags} docs
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}

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
%{_qt5_libdir}/libQt5Svg.so.5*
%{_qt5_plugindir}/iconengines/libqsvgicon.so
%{_qt5_plugindir}/imageformats/libqsvg.so
%dir %{_qt5_libdir}/cmake/Qt5Svg/
%{_qt5_libdir}/cmake/Qt5Svg/Qt5Svg_*Plugin.cmake

%files dev
%{_qt5_headerdir}/QtSvg/
%{_qt5_libdir}/libQt5Svg.so
%{_qt5_libdir}/libQt5Svg.prl
%{_qt5_libdir}/cmake/Qt5Svg/Qt5SvgConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Svg.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_svg*.pri

%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtsvg.qch
%{_qt5_docdir}/qtsvg/

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
