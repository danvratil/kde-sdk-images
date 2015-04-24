%global qt_module qtwebkit

%global _hardened_build 1

Summary: Qt5 - QtWebKit components
Name:    qt5-qtwebkit%{?bootstrap:-bootstrap}
Version: 5.4.1
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# Search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch1: qtwebkit-opensource-src-5.2.0-pluginpath.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3: qtwebkit-opensource-src-5.0.1-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4: qtwebkit-opensource-src-5.2.0-save_memory.patch

# Add AArch64 support
Patch7: 0001-Add-ARM-64-support.patch

# truly madly deeply no rpath please, kthxbye
Patch8: qtwebkit-opensource-src-5.2.1-no_rpath.patch

# fix GMutexLocker build issue
Patch9: qtwebkit-opensource-src-5.4.0-mutexlocker.patch

# fix gcc5 template issue
Patch10: qt5-qtwebkit-gcc5.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1204795
# https://codereview.qt-project.org/#/c/108936/
Patch11: qtwebkit-opensource-src-5.4.1-private_browsing.patch

BuildRequires: qt5-qtbase%{?bootstrap:-bootstrap}-dev
BuildRequires: qt5-qtdeclarative%{?bootstrap:-bootstrap}-dev
BuildRequires: qt5-qtlocation%{?bootstrap:-bootstrap}-dev
BuildRequires: qt5-qtsensors%{?bootstrap:-bootstrap}-dev

BuildRequires: freedesktop-sdk-base

BuildRequires: gstreamer1-dev
BuildRequires: gstreamer1-plugins-base-dev

BuildRequires: libXrender-dev
BuildRequires: glib2-dev
BuildRequires: mesa-libGL-dev
BuildRequires: pcre16-dev
BuildRequires: libXcomposite-dev
BuildRequires: libXrender-dev

#BuildRequires: pkgconfig(libudev)
#BuildRequires: ruby

%{?_qt5_version:Requires: qt5-qtbase%{?bootstrap:-bootstrap}%{?_isa} >= %{_qt5_version}}

##upstream patches

%description
%{summary}

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase%{?bootstrap:-bootstrap}-dev%{?_isa}
Requires: qt5-qtdeclarative%{?bootstrap:-bootstrap}-dev%{?_isa}
%description dev
%{summary}.

%if ! 0%{?bootstrap}
%package doc
Summary: API documentation for %{name}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%setup -q -n qtwebkit-opensource-src-%{version}%{?pre:-%{pre}}

%patch1 -p1 -b .pluginpath
%patch3 -p1 -b .debuginfo
%patch4 -p1 -b .save_memory

%patch7 -p1 -b .aarch64
%patch8 -p1 -b .no_rpath
%patch9 -p1 -b .MutexLocker
%patch10 -p1 -b .gcc5-template
%patch11 -p1 -b .private_browsing

echo "nuke bundled code..."
# nuke bundled code
mkdir Source/ThirdParty/orig
mv Source/ThirdParty/{gtest/,qunit/} \
   Source/ThirdParty/orig/

%build
mkdir %{_target_platform}
pushd %{_target_platform}

%{qmake_qt5} .. \
	%{?system_angle:DEFINES+=USE_SYSTEM_ANGLE=1} \
%ifnarch %{arm} %{ix86} x86_64
	DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0
%endif

# workaround, disable parallel compilation as it fails to compile in brew
make %{?_smp_mflags}
#make -j2

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
%doc Source/WebCore/LICENSE*
%doc ChangeLog* VERSION
%{_qt5_libdir}/libQt5WebKit.so.5*
%{_qt5_libdir}/libQt5WebKitWidgets.so.5*
%{_qt5_libexecdir}/QtWebPluginProcess
%{_qt5_libexecdir}/QtWebProcess
%{_qt5_archdatadir}/qml/QtWebKit/

%files dev
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if ! 0%{?bootstrap}
%files doc
%{_qt5_docdir}/qtwebkit.qch
%{_qt5_docdir}/qtwebkit/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
