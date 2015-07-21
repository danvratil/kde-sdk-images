%global qt_module qtconnectivity

Summary: Qt5 - Connectivity components
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

## upstreamable patches
# bswap_16 apparently missing on el6/ppc64
Patch50: qtconnectivity-opensource-src-5.4.0-bswap_16.patch

BuildRequires: freedesktop-sdk-base

BuildRequires: qt5-qtbase-dev
BuildRequires: qt5-qtdeclarative-dev

BuildRequires: bluez-libs-dev

Requires: bluez

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

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

%patch50 -p1 -b .bswap_16


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

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
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
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_bindir}/sdpscanner
%{_qt5_bindir}/sdpscanner
%{_qt5_libdir}/libQt5Bluetooth.so.5*
%{_qt5_archdatadir}/qml/QtBluetooth/
%{_qt5_libdir}/libQt5Nfc.so.5*
%{_qt5_archdatadir}/qml/QtNfc/

%files dev
%{_qt5_headerdir}/QtBluetooth/
%{_qt5_libdir}/libQt5Bluetooth.so
%{_qt5_libdir}/libQt5Bluetooth.prl
%dir %{_qt5_libdir}/cmake/Qt5Bluetooth/
%{_qt5_libdir}/cmake/Qt5Bluetooth/Qt5BluetoothConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Bluetooth.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_bluetooth*.pri
%{_qt5_headerdir}/QtNfc/
%{_qt5_libdir}/libQt5Nfc.so
%{_qt5_libdir}/libQt5Nfc.prl
%dir %{_qt5_libdir}/cmake/Qt5Nfc/
%{_qt5_libdir}/cmake/Qt5Nfc/Qt5NfcConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Nfc.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_nfc*.pri

%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtbluetooth.qch
%{_qt5_docdir}/qtbluetooth/
%{_qt5_docdir}/qtnfc.qch
%{_qt5_docdir}/qtnfc/

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- initial version (forked from Fedora)
