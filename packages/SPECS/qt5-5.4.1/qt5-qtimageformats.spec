%global qt_module qtimageformats

%global have_jasper 0

Summary: Qt5 - QtImageFormats component
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base

BuildRequires: qt5-qtbase-dev

BuildRequires: libmng-dev
%if 0%{?have_jasper}
BuildRequires: jasper-dev
%endif

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The core Qt Gui library by default supports reading and writing image
files of the most common file formats: PNG, JPEG, BMP, GIF and a few more,
ref. Reading and Writing Image Files. The Qt Image Formats add-on module
provides optional support for other image file formats, including:
MNG, TGA, TIFF, WBMP.

%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

# Remove webp
rm -rv src/3rdparty

# Otherwise it will try to build against the bundled one which we remove above
%if ! 0%{?build_jasper}
sed -i "s/jp2//" src/plugins/imageformats/imageformats.pro
%endif

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


%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_qt5_plugindir}/imageformats/libqmng.so
%{_qt5_plugindir}/imageformats/libqtga.so
%{_qt5_plugindir}/imageformats/libqtiff.so
%{_qt5_plugindir}/imageformats/libqwbmp.so
%{_qt5_plugindir}/imageformats/libqdds.so
%{_qt5_plugindir}/imageformats/libqicns.so
%if 0%{?have_jasper}
%{_qt5_plugindir}/imageformats/libqjp2.so
%endif
%{_qt5_plugindir}/imageformats/libqwebp.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*Plugin.cmake

%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtimageformats.qch
%{_qt5_docdir}/qtimageformats/


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
