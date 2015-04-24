%global qt_module qtscript

Summary: Qt5 - QtScript component
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: qt5-qtbase-dev
BuildRequires: qt5-qttools-dev
BuildRequires: qt5-qttools-static

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

## .prl file love (maybe consider just deleting these -- rex
# nuke dangling reference(s) to %%buildroot, excessive (.la-like) libs
sed -i \
  -e "/^QMAKE_PRL_BUILD_DIR/d" \
  -e "/^QMAKE_PRL_LIBS/d" \
  %{buildroot}%{_qt5_libdir}/*.prl

## unpackaged files
# .la files, die, die, die.
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt5Script.so.5*
%{_qt5_libdir}/libQt5ScriptTools.so.5*

%files dev
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5Script.so
%{_qt5_libdir}/libQt5Script.prl
%{_qt5_libdir}/libQt5ScriptTools.so
%{_qt5_libdir}/libQt5ScriptTools.prl
%dir %{_qt5_libdir}/cmake/Qt5Script/
%{_qt5_libdir}/cmake/Qt5Script/Qt5ScriptConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5ScriptTools/
%{_qt5_libdir}/cmake/Qt5ScriptTools/Qt5ScriptToolsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files doc
%{_qt5_docdir}/qtscript.qch
%{_qt5_docdir}/qtscript/
%{_qt5_docdir}/qtscripttools.qch
%{_qt5_docdir}/qtscripttools/

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
