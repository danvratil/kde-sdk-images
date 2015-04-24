%global qt_module qtquick1

Summary: A declarative language for describing user interfaces in Qt5
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: qt5-qtbase-dev
BuildRequires: qt5-qtscript-dev
BuildRequires: qt5-qttools-dev
BuildRequires: qt5-qtwebkit-dev
BuildRequires: qt5-qtxmlpatterns-dev

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
Qt Quick is a collection of technologies that are designed to help
developers create the kind of intuitive, modern, fluid user interfaces
that are increasingly used on mobile phones, media players, set-top
boxes and other portable devices.

Qt Quick consists of a rich set of user interface elements, a declarative
language for describing user interfaces and a language runtime. A
collection of C++ APIs is used to integrate these high level features
with classic Qt applications.

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-dev%{?_isa}
%description dev
%{summary}.

#%package doc
#Summary: API documentation for %{name}
#Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
#BuildRequires: qt5-qttools-dev
#BuildArch: noarch
#%description doc
#%{summary}.

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
#make %{?_smp_mflags} docs
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}
#make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}

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
%doc LICENSE.GPL* LICENSE.LGPL* LGPL_EXCEPTION.txt
%{_qt5_libdir}/libQt5Declarative.so.5*
%{_qt5_importdir}/Qt/
%{_qt5_importdir}/QtWebKit/
%{_qt5_importdir}/builtins.qmltypes
%{_qt5_plugindir}/designer/*.so
%{_qt5_plugindir}/qml1tooling/
%dir %{_qt5_libdir}/cmake/Qt5Declarative/
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5Declarative_QTcpServerConnection.cmake
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5Declarative_QtQuick1Plugin.cmake
%dir %{_qt5_libdir}/cmake/Qt5Designer/
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QDeclarativeViewPlugin.cmake

%files dev
%{_qt5_bindir}/qml1plugindump*
%{_qt5_bindir}/qmlviewer*
%{_bindir}/qml1plugindump*
%{_bindir}/qmlviewer*
%{_qt5_headerdir}/QtDeclarative/
%{_qt5_libdir}/libQt5Declarative.so
%{_qt5_libdir}/libQt5Declarative.prl
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5DeclarativeConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Declarative.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_declarative*.pri

#%files doc
#%{_qt5_docdir}/*

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)

