%global qt_module qttools

Summary: Qt5 - QtTool components
Name:    qt5-qttools%{?bootstrap:-bootstrap}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

#Patch1: qttools-opensource-src-5.3.2-system-clucene.patch

## upstream patches

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

BuildRequires:  freedesktop-sdk-base

BuildRequires:  desktop-file-utils

# Build even the non-bootstrapped version against bootstrapped packages
# that means we will be able to build qt5-qtbase against non-bootstrapped
# qt5-qttools
BuildRequires:  qt5-qtbase-bootstrap-dev
BuildRequires:  qt5-qtdeclarative-bootstrap-dev
BuildRequires:  qt5-qtdeclarative-bootstrap-static
BuildRequires:  qt5-qtwebkit-bootstrap-dev
%if ! 0%{?bootstrap}
BuildRequires:  qt5-qttools-bootstrap-dev
%endif

BuildRequires:  clucene-core-dev

Requires: %{name}-common = %{version}-%{release}
%{?_qt5_version:Requires: qt5-qtbase%{?bootstrap:-bootstrap}%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch
%description common
%{summary}.

%package dev
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-clucene%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase%{?bootstrap:-bootstrap}-dev%{?_isa}
Provides: qt5%{?bootstrap:-bootstrap}-designer = %{version}-%{release}
Provides: qt5%{?bootstrap:-bootstrap}-linguist = %{version}-%{release}
%description dev
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-dev%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-clucene
Summary: Qt5 CLucene runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-clucene
%{summary}.

%package libs-designer
Summary: Qt5 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt5 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designercomponents
%{summary}.

%package libs-help
Summary: Qt5 Help runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-help
%{summary}.

%package -n qt5%{?bootstrap:-bootstrap}-assistant
Summary: Documentation browser for Qt5
Requires: %{name}-common = %{version}-%{release}
%description -n qt5%{?bootstrap:-bootstrap}-assistant
%{summary}.

%package -n qt5%{?bootstrap:-bootstrap}-designer-plugin-webkit
Summary: Qt5 designer plugin for WebKit
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
%description -n qt5%{?bootstrap:-bootstrap}-designer-plugin-webkit
%{summary}.

%package -n qt5%{?bootstrap:-bootstrap}-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt5_version:Requires: qt5-qtbase%{?bootstrap:-bootstrap}%{?_isa} >= %{_qt5_version}}
%description -n qt5%{?bootstrap:-bootstrap}-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%if ! 0%{?bootstrap}
%package doc
Summary: API documentation for %{name}
# for qhelpgenerator
BuildRequires: qt5-qttools-bootstrap-dev
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n qttools-opensource-src-%{version}%{?pre:-%{pre}}

#%patch1 -p1 -b .system_clucene
# bundled libs
#rm -rf src/assistant/3rdparty/clucene
#%patch2 -p1 -b .qmake-qt5


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

# Add desktop files, --vendor=qt4 helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt5" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}

# icons
install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant.png
install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/designer.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist.png
done

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

%check
export CMAKE_PREFIX_PATH=%{buildroot}%{_qt5_prefix}:%{buildroot}%{_prefix}
export PATH=%{buildroot}%{_qt5_bindir}:%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
mkdir tests/auto/cmake/%{_target_platform}
pushd tests/auto/cmake/%{_target_platform}
cmake ..
ctest --output-on-failure ||:
popd


%files
%{_bindir}/qdbus
%{_bindir}/qtpaths
%{_qt5_bindir}/qdbus
%{_qt5_bindir}/qtpaths

%files common
%doc LGPL_EXCEPTION.txt LICENSE.LGPL*

%post   libs-clucene -p /sbin/ldconfig
%postun libs-clucene -p /sbin/ldconfig
%files  libs-clucene
%{_qt5_libdir}/libQt5CLucene.so.5*

%post   libs-designer -p /sbin/ldconfig
%postun libs-designer -p /sbin/ldconfig
%files  libs-designer
%{_qt5_libdir}/libQt5Designer.so.5*
%dir %{_qt5_libdir}/cmake/Qt5Designer/

%post   libs-designercomponents -p /sbin/ldconfig
%postun libs-designercomponents -p /sbin/ldconfig
%files  libs-designercomponents
%{_qt5_libdir}/libQt5DesignerComponents.so.5*

%post   libs-help -p /sbin/ldconfig
%postun libs-help -p /sbin/ldconfig
%files  libs-help
%{_qt5_libdir}/libQt5Help.so.5*

%post -n qt5%{?bootstrap:-bootstrap}-assistant
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5%{?bootstrap:-bootstrap}-assistant
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5%{?bootstrap:-bootstrap}-assistant
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n qt5%{?bootstrap:-bootstrap}-assistant
%{_bindir}/assistant
%{_qt5_bindir}/assistant
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*.*

%files -n qt5%{?bootstrap:-bootstrap}-designer-plugin-webkit
%{_qt5_plugindir}/designer/libqwebview.so
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QWebViewPlugin.cmake

%post -n qt5%{?bootstrap:-bootstrap}-qdbusviewer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5%{?bootstrap:-bootstrap}-qdbusviewer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5%{?bootstrap:-bootstrap}-qdbusviewer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n qt5%{?bootstrap:-bootstrap}-qdbusviewer
%{_bindir}/qdbusviewer
%{_qt5_bindir}/qdbusviewer
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%post dev
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans dev
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun dev
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files dev
%{_bindir}/designer
%{_bindir}/lconvert
%{_bindir}/linguist
%{_bindir}/lrelease
%{_bindir}/lupdate
%{_bindir}/pixeltool
%{_bindir}/qcollectiongenerator
%{_bindir}/qhelpconverter
%{_bindir}/qhelpgenerator
%{_bindir}/qtdiag
%{_qt5_bindir}/designer
%{_qt5_bindir}/lconvert
%{_qt5_bindir}/linguist
%{_qt5_bindir}/lrelease
%{_qt5_bindir}/lupdate
%{_qt5_bindir}/pixeltool
%{_qt5_bindir}/qtdiag
%{_qt5_bindir}/qcollectiongenerator
%{_qt5_bindir}/qhelpconverter
%{_qt5_bindir}/qhelpgenerator
%{_qt5_headerdir}/QtCLucene/
%{_qt5_headerdir}/QtDesigner/
%{_qt5_headerdir}/QtDesignerComponents/
%{_qt5_headerdir}/QtHelp/
# phrasebooks used by linguist
%{_qt5_datadir}/phrasebooks/
%{_qt5_libdir}/libQt5CLucene.prl
%{_qt5_libdir}/libQt5CLucene.so
%{_qt5_libdir}/libQt5Designer*.prl
%{_qt5_libdir}/libQt5Designer*.so
%{_qt5_libdir}/libQt5Help.prl
%{_qt5_libdir}/libQt5Help.so
%{_qt5_libdir}/cmake/Qt5Designer/Qt5DesignerConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5Help/
%{_qt5_libdir}/cmake/Qt5Help/Qt5HelpConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5LinguistTools/
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsMacros.cmake
%{_qt5_libdir}/pkgconfig/Qt5CLucene.pc
%{_qt5_libdir}/pkgconfig/Qt5Designer.pc
%{_qt5_libdir}/pkgconfig/Qt5DesignerComponents.pc
%{_qt5_libdir}/pkgconfig/Qt5Help.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_datadir}/applications/*designer.desktop
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%{_datadir}/icons/hicolor/*/apps/linguist*.*

# example designer plugins
%{_qt5_plugindir}/designer/libcontainerextension.so
%{_qt5_plugindir}/designer/libcustomwidgetplugin.so
%{_qt5_plugindir}/designer/libtaskmenuextension.so
%{_qt5_plugindir}/designer/libworldtimeclockplugin.so
%{_qt5_plugindir}/designer/libqquickwidget.so
%dir %{_qt5_libdir}/cmake/Qt5Designer/
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_AnalogClockPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_MultiPageWidgetPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QQuickWidgetPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_TicTacToePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_WorldTimeClockPlugin.cmake

%files static
%{_qt5_headerdir}/QtUiTools/
%{_qt5_libdir}/libQt5UiTools.*a
%{_qt5_libdir}/libQt5UiTools.prl
%{_qt5_libdir}/cmake/Qt5UiTools/
%{_qt5_libdir}/pkgconfig/Qt5UiTools.pc

%if ! 0%{?bootstrap}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtassistant.qch
%{_qt5_docdir}/qtassistant/
%{_qt5_docdir}/qtdesigner.qch
%{_qt5_docdir}/qtdesigner/
%{_qt5_docdir}/qthelp.qch
%{_qt5_docdir}/qthelp/
%{_qt5_docdir}/qtlinguist.qch
%{_qt5_docdir}/qtlinguist/
%{_qt5_docdir}/qtuitools.qch
%{_qt5_docdir}/qtuitools/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
