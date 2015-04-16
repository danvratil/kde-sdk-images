
%global qt_module qtwayland

Summary:        Qt5 - Wayland platform support and QtCompositor module
Name:           qt5-%{qt_module}
Version:        5.4.1
Release:        1%{?dist}
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://qt-project.org/wiki/QtWayland
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.4/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:        Examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

# Presence of .git/ qmake into invoking syncqt for us with
# correct arguments at make time.
# else, out-of-src-tree builds fail with stuff like:
# qwaylanddisplay_p.h:52:54: fatal error: QtWaylandClient/private/qwayland-wayland.h: No such file or directory
# #include <QtWaylandClient/private/qwayland-wayland.h>
mkdir .git


%build
# build support for non-egl platforms
mkdir nogl
pushd nogl
%{qmake_qt5} QT_WAYLAND_GL_CONFIG=nogl ..
popd
make %{?_smp_mflags} -C nogl

%{_qt5_qmake} CONFIG+=wayland-compositor
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot} -C nogl/
make install INSTALL_ROOT=%{buildroot}

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


# install private headers... needed by hawaii shell
install -pm644 \
  include/QtCompositor/%{version}/QtCompositor/private/{wayland-wayland-server-protocol.h,qwayland-server-wayland.h} \
  %{buildroot}%{_qt5_headerdir}/QtCompositor/%{version}/QtCompositor/private/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%doc LICENSE.LGPL* LICENSE.GPL* LGPL_EXCEPTION.txt
%{_qt5_libdir}/libQt5Compositor.so.5*
%{_qt5_libdir}/libQt5WaylandClient.so.5*
%dir %{_qt5_plugindir}/wayland-decoration-client/
%{_qt5_plugindir}/wayland-decoration-client/libbradient.so
%{_qt5_plugindir}/wayland-graphics-integration-server
%{_qt5_plugindir}/wayland-graphics-integration-client
%{_qt5_plugindir}/platforms/libqwayland-egl.so
%{_qt5_plugindir}/platforms/libqwayland-generic.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite-egl.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite-glx.so
%dir %{_qt5_libdir}/cmake/Qt5Compositor/
%{_qt5_libdir}/cmake/Qt5Compositor/Qt5Compositor_*.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*.cmake
%dir %{_qt5_libdir}/cmake/Qt5WaylandClient/
%{_qt5_libdir}/cmake/Qt5WaylandClient/Qt5WaylandClient_*.cmake

%files devel
%{_qt5_bindir}/qtwaylandscanner
%{_qt5_headerdir}/QtCompositor/
%{_qt5_headerdir}/QtWaylandClient/
%{_qt5_libdir}/libQt5Compositor.so
%{_qt5_libdir}/libQt5WaylandClient.so
%{_qt5_libdir}/libQt5Compositor.prl
%{_qt5_libdir}/libQt5WaylandClient.prl
%{_qt5_libdir}/cmake/Qt5Compositor/Qt5CompositorConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Compositor.pc
%{_qt5_libdir}/pkgconfig/Qt5WaylandClient.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_compositor*.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_waylandclient*.pri

%files examples
%{_qt5_examplesdir}/wayland/


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
