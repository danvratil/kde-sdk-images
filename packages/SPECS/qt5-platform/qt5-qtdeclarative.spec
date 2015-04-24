%global qt_module qtdeclarative

Summary: Qt5 - QtDeclarative component
Name:    qt5-%{qt_module}%{?bootstrap:-bootstrap}
Version: 5.4.1
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# FIXME?  now bases on whether qtbase supports sse2 (or not)
# support no_sse2 CONFIG (fedora i686 builds cannot assume -march=pentium4 -msse2 -mfpmath=sse flags, or the JIT that needs them)
# https://codereview.qt-project.org/#change,73710
Patch1: qtdeclarative-opensource-src-5.2.0-no_sse2.patch

Obsoletes: qt5-qtjsbackend < 5.2.0

BuildRequires: freedesktop-sdk-base

BuildRequires: qt5-qtbase%{?bootstrap:-bootstrap}-dev
BuildRequires: qt5-qtxmlpatterns%{?bootstrap:-bootstrap}-dev


%{?_qt5_version:Requires: qt5-qtbase%{?bootstrap:-bootstrap}%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package dev
Summary: Development files for %{name}
Obsoletes: qt5-qtjsbackend-devel < 5.2.0
Requires: %{name}%{?_isa} = %{version}-%{release}
%description dev
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-dev%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%if ! 0%{?bootstrap}
%package doc
Summary: API documentation for %{name}
License: GFDL
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

#patch1 -p1 -b .no_sse2


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

#ifarch %{ix86}
%if 0
# build libQt5Qml with no_sse2
mkdir -p %{_target_platform}-no_sse2
pushd    %{_target_platform}-no_sse2
%{_qt5_qmake} -config no_sse2 ..
make sub-src-clean
make %{?_smp_mflags} -C src/qml
popd
%endif

%if ! 0%{?bootstrap}
make %{?_smp_mflags} docs -C %{_target_platform}
%endif


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%if ! 0%{?bootstrap}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

# hardlink files to %{_bindir}
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  ln -v  ${i} %{buildroot}%{_bindir}/${i}
done
popd

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
%doc LICENSE.GPL* LICENSE.LGPL* LGPL_EXCEPTION.txt
%doc dist/changes*
%{_qt5_libdir}/libQt5Qml.so.5*
#%{_qt5_libdir}/sse2/libQt5Qml.so.5*
%{_qt5_libdir}/libQt5Quick.so.5*
%{_qt5_libdir}/libQt5QuickWidgets.so.5*
%{_qt5_libdir}/libQt5QuickParticles.so.5*
%{_qt5_libdir}/libQt5QuickTest.so.5*
%{_qt5_plugindir}/qmltooling/
%{_qt5_archdatadir}/qml/
%dir %{_qt5_libdir}/cmake/Qt5Qml/
%{_qt5_libdir}/cmake/Qt5Qml/Qt5Qml_QTcpServerConnection.cmake
%{_qt5_libdir}/cmake/Qt5Qml/Qt5Qml_QtQuick2Plugin.cmake

%files dev
%{_bindir}/qml*
%{_qt5_bindir}/qml*
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5Qml.so
%{_qt5_libdir}/libQt5Qml.prl
%{_qt5_libdir}/libQt5Quick*.so
%{_qt5_libdir}/libQt5QuickWidgets.so.5
%{_qt5_libdir}/libQt5Quick*.prl
%dir %{_qt5_libdir}/cmake/Qt5Quick*/
%{_qt5_libdir}/cmake/Qt5*/Qt5*Config*.cmake
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files static
%{_qt5_libdir}/libQt5QmlDevTools.*a
%{_qt5_libdir}/libQt5QmlDevTools.prl

%if ! 0%{?bootstrap}
%files doc
%{_qt5_docdir}/qtqml.qch
%{_qt5_docdir}/qtqml/
%{_qt5_docdir}/qtquick.qch
%{_qt5_docdir}/qtquick/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Initial version (forked from Fedora)

