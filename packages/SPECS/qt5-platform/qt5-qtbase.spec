%global qt_module qtbase

# TODO
%global build_mariadb 0
%global build_postgresql 0
%global build_firebird 0
%global build_odbc 0
%global build_tds 0
%global build_cups 0

%global build_glxutils 0

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Summary: Qt5 - QtBase components
Name:    qt5-qtbase%{?bootstrap:-bootstrap}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1036956
Source5: qconfig-multilib.h

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt5-check-opengl2.sh

# support multilib optflags
Patch2: qtbase-multilib_optflags.patch

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch4: qtbase-opensource-src-5.3.2-QTBUG-35459.patch

# unconditionally enable freetype lcdfilter support
Patch12: qtbase-opensource-src-5.2.0-enable_ft_lcdfilter.patch

# upstreamable patches
# support poll
# https://bugreports.qt-project.org/browse/QTBUG-27195
# NEEDS REBASE
Patch50: qt5-poll.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1083664
# https://bugreports.qt.io/browse/QTBUG-42985
Patch51: qtbase-opensource-src-5.4.0-QTBUG-42985.patch

# Qt 5.5 patches
Patch208: qt5-qtbase-5.5-Get_display_number_when_screen_number_is_omitted.patch


Patch209: qt5-qtbase-xsettings-dpr.patch


Patch212: 0012-Fix-a-crash-in-QPlainTextEdit-documentChanged.patch
Patch272: 0072-CMake-Fix-QObject-connect-failing-on-ARM.patch
Patch294: 0094-Fix-Meta-.-shortcuts-on-XCB.patch
Patch332: 0132-Call-ofono-nm-Registered-delayed-in-constructor-othe.patch
Patch336: 0136-Make-sure-there-s-a-scene-before-using-it.patch
# http://lists.qt-project.org/pipermail/announce/2015-February/000059.html
# CVE-2015-0295
Patch349: 0149-Fix-a-division-by-zero-when-processing-malformed-BMP.patch

# macros, be mindful to keep sync'd with macros.qt5
Source1: macros.qt5
%define _qt5 %{name}
%define _qt5_prefix %{_libdir}/qt5
%define _qt5_archdatadir %{_libdir}/qt5
# -devel bindir items (still) conflict with qt4
# at least until this is all implemented,
# http://lists.qt-project.org/pipermail/development/2012-November/007990.html
#define _qt5_bindir %{_bindir}
%define _qt5_bindir %{_qt5_prefix}/bin
%define _qt5_datadir %{_datadir}/qt5
%define _qt5_docdir %{_docdir}/qt5
%define _qt5_examplesdir %{_qt5_prefix}/examples
%define _qt5_headerdir %{_includedir}/qt5
%define _qt5_importdir %{_qt5_archdatadir}/imports
%define _qt5_libdir %{_libdir}
%define _qt5_libexecdir %{_qt5_archdatadir}/libexec
%define _qt5_plugindir %{_qt5_archdatadir}/plugins
%define _qt5_settingsdir %{_sysconfdir}/xdg
%define _qt5_sysconfdir %{_qt5_settingsdir}
%define _qt5_translationdir %{_datadir}/qt5/translations

# Do not check any files in %%{_qt5_plugindir}/platformthemes/ for requires.
# Those themes are there for platform integration. If the required libraries are
# not there, the platform to integrate with isn't either. Then Qt will just
# silently ignore the plugin that fails to load. Thus, there is no need to let
# RPM drag in gtk2 as a dependency for the GTK+ 2 dialog support.
%global __requires_exclude_from ^%{_qt5_plugindir}/platformthemes/.*$

BuildRequires: freedesktop-sdk-base
BuildRequires: cmake
%if 0%{?build_cups}
BuildRequires: cups-dev
%endif
BuildRequires: alsa-lib-dev
BuildRequires: dbus-dev
BuildRequires: libdrm-dev
BuildRequires: mesa-libGL-dev
BuildRequires: glib2-dev
BuildRequires: gtk2-dev

BuildRequires: libICE-dev
BuildRequires: libSM-dev

#BuildRequires: libudev-dev
#BuildRequires: NetworkManager-dev
#BuildRequires: pulseaudio-mainloop-glib
#BuildRequires: libxcb-xkb-dev

BuildRequires: xkeyboard-config-dev

BuildRequires: at-spi2-core-dev
BuildRequires: mesa-libEGL-dev
#BuildRequires: glesv2

BuildRequires: harfbuzz-dev
BuildRequires: pcre16-dev

BuildRequires: libxcb-dev
BuildRequires: libxkbcommon-dev
BuildRequires: libxkbcommon-x11-dev

BuildRequires: xcb-util-wm-dev
BuildRequires: xcb-util-image-dev
BuildRequires: xcb-util-keysyms-dev
BuildRequires: xcb-util-renderutil-dev

Conflicts: qt < 1:4.8.6-10

# workaround gold linker bug by not using it
# https://bugzilla.redhat.com/show_bug.cgi?id=1193044
#https://sourceware.org/bugzilla/show_bug.cgi?id=16992
%define use_gold_linker -no-use-gold-linker

%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
Requires: mesa-libEGL-dev
Requires: mesa-libGL-dev
%description dev
%{summary}.

%if ! 0%{?bootstrap}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
# always use the bootstrap version, because non-bootstrapped
# qt5-qttools require qt5-qtbase
BuildRequires: qt5-qttools-bootstrap-dev
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-dev%{?_isa} = %{version}-%{release}
Requires: fontconfig-dev
Requires: glib2-dev
%description static
%{summary}.

%if 0%{?build_mariadb}
%package ibase
Summary: IBase driver for Qt5's SQL classes
BuildRequires: firebird-dev
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%if 0%{?build_firebird}
%package mysql
Summary: MySQL driver for Qt5's SQL classes
BuildRequires: mysql-dev
Requires: %{name}%{?_isa} = %{version}-%{release}
%description mysql
%{summary}.
%endif

%if 0%{?build_odbc}
%package odbc
Summary: ODBC driver for Qt5's SQL classes
BuildRequires: unixODBC-dev
Requires: %{name}%{?_isa} = %{version}-%{release}
%description odbc
%{summary}.
%endif

%if 0%{?build_postgresql}
%package postgresql
Summary: PostgreSQL driver for Qt5's SQL classes
BuildRequires: postgresql-dev
Requires: %{name}%{?_isa} = %{version}-%{release}
%description postgresql
%{summary}.
%endif

%if 0%{?build_tds}
%package tds
Summary: TDS driver for Qt5's SQL classes
BuildRequires: freetds-dev
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tds
%{summary}.
%endif

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt5 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%if 0%{build_glxutils}
# for Source6: 10-qt5-check-opengl2.sh:
# glxinfo
Requires: glx-utils
%endif

%description gui
Qt5 libraries used for drawing widgets and OpenGL items.


%prep
%setup -q -n qtbase-opensource-src-%{version}%{?pre:-%{pre}}

%patch2 -p1 -b .multilib_optflags
# drop backup file(s), else they get installed too, http://bugzilla.redhat.com/639463
rm -fv mkspecs/linux-g++*/qmake.conf.multilib-optflags

%patch4 -p1 -b .QTBUG-35459
%patch12 -p1 -b .enable_ft_lcdfilter

#patch50 -p1 -b .poll
%patch51 -p1 -b .QTBUG-42985

%patch208 -p1 -b .ibus_get_display_number

%patch209 -p1 -b .dpr-xsettings

%patch212 -p1 -b .0012
%patch272 -p1 -b .0072
%patch294 -p1 -b .0094
%patch332 -p1 -b .0132
%patch336 -p1 -b .0136
%patch349 -p1 -b .0149

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%define platform linux-g++

sed -i -e "s|-O2|$RPM_OPT_FLAGS|g" \
  mkspecs/%{platform}/qmake.conf

sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 $RPM_LD_FLAGS|" \
  mkspecs/common/g++-unix.conf

# undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#1065636)
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf

# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
mv sqlite freetype libjpeg libpng zlib xcb UNUSED/
popd


# builds failing mysteriously on f20
# ./configure: Permission denied
# check to ensure that can't happen -- rex
test -x configure || chmod +x configure

%build

./configure -v \
  -confirm-license \
  -opensource \
  -prefix %{_qt5_prefix} \
  -archdatadir %{_qt5_archdatadir} \
  -bindir %{_qt5_bindir} \
  -datadir %{_qt5_datadir} \
  -docdir %{_qt5_docdir} \
  -examplesdir %{_qt5_examplesdir} \
  -headerdir %{_qt5_headerdir} \
  -importdir %{_qt5_importdir} \
  -libdir %{_qt5_libdir} \
  -libexecdir %{_qt5_libexecdir} \
  -plugindir %{_qt5_plugindir} \
  -sysconfdir %{_qt5_sysconfdir} \
  -translationdir %{_qt5_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -accessibility \
  -dbus-linked \
  -fontconfig \
  -glib \
  -gtkstyle \
  -iconv \
  -icu \
  -openssl-linked \
  -optimized-qmake \
  -nomake tests \
  -no-pch \
  -no-rpath \
  -no-separate-debug-info \
  -no-strip \
  -system-harfbuzz \
  -system-libjpeg \
  -system-libpng \
  -system-pcre \
  -system-sqlite \
  -system-xkbcommon \
  -system-zlib \
  %{?use_gold_linker}

make %{?_smp_mflags}

%if ! 0%{?bootstrap}
# wierd but necessary, to force regeration to use just-built qdoc
rm -fv src/corelib/Makefile
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

make install_docs INSTALL_ROOT=%{buildroot}

# Qt5.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt5.pc<<EOF
prefix=%{_qt5_prefix}
archdatadir=%{_qt5_archdatadir}
bindir=%{_qt5_bindir}
datadir=%{_qt5_datadir}

docdir=%{_qt5_docdir}
examplesdir=%{_qt5_examplesdir}
headerdir=%{_qt5_headerdir}
importdir=%{_qt5_importdir}
libdir=%{_qt5_libdir}
libexecdir=%{_qt5_libexecdir}
moc=%{_qt5_bindir}/moc
plugindir=%{_qt5_plugindir}
qmake=%{_qt5_bindir}/qmake
settingsdir=%{_qt5_settingsdir}
sysconfdir=%{_qt5_sysconfdir}
translationdir=%{_qt5_translationdir}

Name: Qt5
Description: Qt5 Configuration
Version: %{version}
EOF

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5

# create/own dirs
mkdir -p %{buildroot}{%{_qt5_archdatadir}/mkspecs/modules,%{_qt5_importdir},%{_qt5_libexecdir},%{_qt5_plugindir}/{designer,iconengines,script,styles},%{_qt5_translationdir}}

# hardlink files to %{_bindir}
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  ln -v  ${i} %{buildroot}%{_bindir}/${i}
done
popd

# multilib: qconfig.h
mv %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h %{buildroot}%{_qt5_headerdir}/QtCore/qconfig-%{__isa_bits}.h
install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h

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

%if 0%{build_glxutils}
install -p -m755 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%endif


## work-in-progress, doesn't work yet -- rex
%if 0
%check
export CMAKE_PREFIX_PATH=%{buildroot}%{_prefix}
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
mkdir tests/auto/cmake/%{_target_platform}
pushd tests/auto/cmake/%{_target_platform}
cmake .. ||:
ctest --output-on-failure ||:
popd
%endif


%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files
%doc LICENSE.LGPL* LGPL_EXCEPTION.txt
%{_qt5_libdir}/libQt5Concurrent.so.5*
%{_qt5_libdir}/libQt5Core.so.5*
%{_qt5_libdir}/libQt5DBus.so.5*
%{_qt5_libdir}/libQt5Network.so.5*
%{_qt5_libdir}/libQt5Sql.so.5*
%{_qt5_libdir}/libQt5Test.so.5*
%{_qt5_libdir}/libQt5Xml.so.5*
%dir %{_qt5_libdir}/cmake/
%dir %{_qt5_libdir}/cmake/Qt5/
%dir %{_qt5_libdir}/cmake/Qt5Concurrent/
%dir %{_qt5_libdir}/cmake/Qt5Core/
%dir %{_qt5_libdir}/cmake/Qt5DBus/
%dir %{_qt5_libdir}/cmake/Qt5Gui/
%dir %{_qt5_libdir}/cmake/Qt5Network/
%dir %{_qt5_libdir}/cmake/Qt5OpenGL/
%dir %{_qt5_libdir}/cmake/Qt5PrintSupport/
%dir %{_qt5_libdir}/cmake/Qt5Sql/
%dir %{_qt5_libdir}/cmake/Qt5Test/
%dir %{_qt5_libdir}/cmake/Qt5Widgets/
%dir %{_qt5_libdir}/cmake/Qt5Xml/
%dir %{_qt5_docdir}/
%{_qt5_docdir}/global/
%{_qt5_importdir}/
%{_qt5_translationdir}/
%dir %{_qt5_prefix}/
%dir %{_qt5_datadir}/
%dir %{_qt5_libexecdir}/
%dir %{_qt5_plugindir}/
%dir %{_qt5_plugindir}/bearer/
%{_qt5_plugindir}/bearer/libqconnmanbearer.so
%{_qt5_plugindir}/bearer/libqgenericbearer.so
%{_qt5_plugindir}/bearer/libqnmbearer.so
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QConnmanEnginePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QGenericEnginePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QNetworkManagerEnginePlugin.cmake
#dir %{_qt5_plugindir}/accessible/
%dir %{_qt5_plugindir}/designer/
%dir %{_qt5_plugindir}/generic/
%dir %{_qt5_plugindir}/iconengines/
%dir %{_qt5_plugindir}/imageformats/
%dir %{_qt5_plugindir}/platforminputcontexts/
%dir %{_qt5_plugindir}/platforms/
%dir %{_qt5_plugindir}/platformthemes/
%if 0%{?build_cups}
%dir %{_qt5_plugindir}/printsupport/
%endif
%dir %{_qt5_plugindir}/script/
%dir %{_qt5_plugindir}/sqldrivers/
%dir %{_qt5_plugindir}/styles/
%{_qt5_plugindir}/sqldrivers/libqsqlite.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake

%if ! 0%{?bootstrap}
%files doc
%doc LICENSE.FDL
%doc dist/README dist/changes-5.*
%{_qt5_docdir}/*.qch
%{_qt5_docdir}/qdoc/
%{_qt5_docdir}/qmake/
%{_qt5_docdir}/qtconcurrent/
%{_qt5_docdir}/qtcore/
%{_qt5_docdir}/qtdbus/
%{_qt5_docdir}/qtgui/
%{_qt5_docdir}/qtnetwork/
%{_qt5_docdir}/qtopengl/
%{_qt5_docdir}/qtplatformheaders/
%{_qt5_docdir}/qtprintsupport/
%{_qt5_docdir}/qtsql/
%{_qt5_docdir}/qttestlib/
%{_qt5_docdir}/qtwidgets/
%{_qt5_docdir}/qtxml/
%endif

%files dev
%{rpm_macros_dir}/macros.qt5
%if "%{_qt5_bindir}" != "%{_bindir}"
%dir %{_qt5_bindir}
%endif
%{_bindir}/moc*
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qdoc*
%{_bindir}/qmake*
%{_bindir}/rcc*
%{_bindir}/syncqt*
%{_bindir}/uic*
%{_bindir}/qlalr
%{_qt5_bindir}/moc*
%{_qt5_bindir}/qdbuscpp2xml*
%{_qt5_bindir}/qdbusxml2cpp*
%{_qt5_bindir}/qdoc*
%{_qt5_bindir}/qmake*
%{_qt5_bindir}/rcc*
%{_qt5_bindir}/syncqt*
%{_qt5_bindir}/uic*
%{_qt5_bindir}/qlalr
%if "%{_qt5_headerdir}" != "%{_includedir}"
%dir %{_qt5_headerdir}
%endif
%{_qt5_headerdir}/QtConcurrent/
%{_qt5_headerdir}/QtCore/
%{_qt5_headerdir}/QtDBus/
%{_qt5_headerdir}/QtGui/
%{_qt5_headerdir}/QtNetwork/
%{_qt5_headerdir}/QtOpenGL/
%{_qt5_headerdir}/QtPlatformHeaders/
%{_qt5_headerdir}/QtPrintSupport/
%{_qt5_headerdir}/QtSql/
%{_qt5_headerdir}/QtTest/
%{_qt5_headerdir}/QtWidgets/
%{_qt5_headerdir}/QtXml/
%{_qt5_archdatadir}/mkspecs/
%{_qt5_libdir}/libQt5Concurrent.prl
%{_qt5_libdir}/libQt5Concurrent.so
%{_qt5_libdir}/libQt5Core.prl
%{_qt5_libdir}/libQt5Core.so
%{_qt5_libdir}/libQt5DBus.prl
%{_qt5_libdir}/libQt5DBus.so
%{_qt5_libdir}/libQt5Gui.prl
%{_qt5_libdir}/libQt5Gui.so
%{_qt5_libdir}/libQt5Network.prl
%{_qt5_libdir}/libQt5Network.so
%{_qt5_libdir}/libQt5OpenGL.prl
%{_qt5_libdir}/libQt5OpenGL.so
%{_qt5_libdir}/libQt5PrintSupport.prl
%{_qt5_libdir}/libQt5PrintSupport.so
%{_qt5_libdir}/libQt5Sql.prl
%{_qt5_libdir}/libQt5Sql.so
%{_qt5_libdir}/libQt5Test.prl
%{_qt5_libdir}/libQt5Test.so
%{_qt5_libdir}/libQt5Widgets.prl
%{_qt5_libdir}/libQt5Widgets.so
%{_qt5_libdir}/libQt5Xml.prl
%{_qt5_libdir}/libQt5Xml.so
%{_qt5_libdir}/cmake/Qt5/Qt5Config*.cmake
%{_qt5_libdir}/cmake/Qt5Concurrent/Qt5ConcurrentConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreMacros.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CTestMacros.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusConfig*.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusMacros.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%{_qt5_libdir}/cmake/Qt5OpenGL/Qt5OpenGLConfig*.cmake
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Test/Qt5TestConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{_qt5_libdir}/cmake/Qt5Xml/Qt5XmlConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5.pc
%{_qt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{_qt5_libdir}/pkgconfig/Qt5Core.pc
%{_qt5_libdir}/pkgconfig/Qt5DBus.pc
%{_qt5_libdir}/pkgconfig/Qt5Gui.pc
%{_qt5_libdir}/pkgconfig/Qt5Network.pc
%{_qt5_libdir}/pkgconfig/Qt5OpenGL.pc
%{_qt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{_qt5_libdir}/pkgconfig/Qt5Sql.pc
%{_qt5_libdir}/pkgconfig/Qt5Test.pc
%{_qt5_libdir}/pkgconfig/Qt5Widgets.pc
%{_qt5_libdir}/pkgconfig/Qt5Xml.pc

%files static
%{_qt5_libdir}/libQt5Bootstrap.*a
%{_qt5_libdir}/libQt5Bootstrap.prl
%{_qt5_libdir}/pkgconfig/Qt5Bootstrap.pc
%{_qt5_headerdir}/QtOpenGLExtensions/
%{_qt5_libdir}/libQt5OpenGLExtensions.*a
%{_qt5_libdir}/libQt5OpenGLExtensions.prl
%{_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_qt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{_qt5_headerdir}/QtPlatformSupport/
%{_qt5_libdir}/libQt5PlatformSupport.*a
%{_qt5_libdir}/libQt5PlatformSupport.prl
%{_qt5_libdir}/pkgconfig/Qt5PlatformSupport.pc

%files examples
%{_qt5_examplesdir}/

%if 0%{?build_odbc}
%files ibase
%{_qt5_plugindir}/sqldrivers/libqsqlibase.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QIBaseDriverPlugin.cmake
%endif

%if 0%{?build_mysql}
%files mysql
%{_qt5_plugindir}/sqldrivers/libqsqlmysql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QMYSQLDriverPlugin.cmake
%endif

%if 0%{?build_odbc}
%files odbc
%{_qt5_plugindir}/sqldrivers/libqsqlodbc.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QODBCDriverPlugin.cmake
%endif

%if 0%{?build_postgresql}
%files postgresql
%{_qt5_plugindir}/sqldrivers/libqsqlpsql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QPSQLDriverPlugin.cmake
%endif

%if 0%{build_tds}
%files tds
%{_qt5_plugindir}/sqldrivers/libqsqltds.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QTDSDriverPlugin.cmake
%endif

%post gui -p /sbin/ldconfig
%postun gui -p /sbin/ldconfig

%files gui
%if 0%{?build_glxutils}
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d/
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%endif
%{_qt5_libdir}/libQt5Gui.so.5*
%{_qt5_libdir}/libQt5OpenGL.so.5*
%{_qt5_libdir}/libQt5PrintSupport.so.5*
%{_qt5_libdir}/libQt5Widgets.so.5*
#{_qt5_plugindir}/accessible/libqtaccessiblewidgets.so
%{_qt5_plugindir}/generic/libqevdevkeyboardplugin.so
%{_qt5_plugindir}/generic/libqevdevmouseplugin.so
%{_qt5_plugindir}/generic/libqevdevtabletplugin.so
%{_qt5_plugindir}/generic/libqevdevtouchplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevKeyboardPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevMousePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTabletPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTouchScreenPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
#%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QKmsIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalEglIntegrationPlugin.cmake
%{_qt5_plugindir}/imageformats/libqgif.so
%{_qt5_plugindir}/imageformats/libqico.so
%{_qt5_plugindir}/imageformats/libqjpeg.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGifPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QICOPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QJpegPlugin.cmake
%{_qt5_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_qt5_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QIbusPlatformInputContextPlugin.cmake
%{_qt5_plugindir}/platforms/libqlinuxfb.so
%{_qt5_plugindir}/platforms/libqminimal.so
%{_qt5_plugindir}/platforms/libqoffscreen.so
%{_qt5_plugindir}/platforms/libqxcb.so
%{_qt5_plugindir}/platforms/libqeglfs.so
#%{_qt5_plugindir}/platforms/libqkms.so
%{_qt5_plugindir}/platforms/libqminimalegl.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLinuxFbIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbIntegrationPlugin.cmake
%{_qt5_plugindir}/platformthemes/libqgtk2.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGtk2ThemePlugin.cmake
%if 0%{?build_cups}
%{_qt5_plugindir}/printsupport/libcupsprintersupport.so
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake
%endif


%changelog
* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- initial version (forked from Fedora)

