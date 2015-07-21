%global qt_module qtserialport

Summary: Qt5 - SerialPort component
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: qt5-qtbase-dev

# FIXME
#BuildRequires: pkgconfig(libudev)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
Qt Serial Port provides the basic functionality, which includes configuring,
I/O operations, getting and setting the control signals of the RS-232 pinouts.

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-dev%{?_isa}
%description dev
%{summary}.

%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.

# no examples yet
%if 0
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt-project.org/browse/QTBUG-42071
QT_HASH_SEED=0; export QT_HASH_SEED
make %{?_smp_mflags} docs
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}

# workaround issue where on some archs/releases doc file is named examples-serialport.html or qtserialport-examples.html
if [ -f %{buildroot}%{_qt5_docdir}/qtserialport/qtserialport-examples.html ]; then
   mv   %{buildroot}%{_qt5_docdir}/qtserialport/qtserialport-examples.html \
        %{buildroot}%{_qt5_docdir}/qtserialport/examples-serialport.html
fi

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
%{_qt5_libdir}/libQt5SerialPort.so.5*

%files dev
%{_qt5_headerdir}/QtSerialPort/
%{_qt5_libdir}/libQt5SerialPort.so
%{_qt5_libdir}/libQt5SerialPort.prl
%dir %{_qt5_libdir}/cmake/Qt5SerialPort/
%{_qt5_libdir}/cmake/Qt5SerialPort/Qt5SerialPortConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5SerialPort.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_serialport*.pri

%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtserialport.qch
%{_qt5_docdir}/qtserialport/

# no examples, yet
%if 0
#if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
