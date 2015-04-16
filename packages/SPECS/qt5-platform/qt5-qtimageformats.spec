
%global qt_module qtimageformats

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

Summary: Qt5 - QtImageFormats component
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.4/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: jasper-devel
BuildRequires: libwebp-devel

# prior -devel subpkg contained only runtime cmake bits
Obsoletes: qt5-qtimageformats-devel < 5.4.0

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The core Qt Gui library by default supports reading and writing image
files of the most common file formats: PNG, JPEG, BMP, GIF and a few more,
ref. Reading and Writing Image Files. The Qt Image Formats add-on module
provides optional support for other image file formats, including:
MNG, TGA, TIFF, WBMP.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

# Remove webp
rm -rv src/3rdparty


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif


%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_qt5_plugindir}/imageformats/libqmng.so
%{_qt5_plugindir}/imageformats/libqtga.so
%{_qt5_plugindir}/imageformats/libqtiff.so
%{_qt5_plugindir}/imageformats/libqwbmp.so
%{_qt5_plugindir}/imageformats/libqdds.so
%{_qt5_plugindir}/imageformats/libqicns.so
%{_qt5_plugindir}/imageformats/libqjp2.so
%{_qt5_plugindir}/imageformats/libqwebp.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*Plugin.cmake

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtimageformats.qch
%{_qt5_docdir}/qtimageformats/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
