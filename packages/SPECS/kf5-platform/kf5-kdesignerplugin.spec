%global framework kdesignerplugin

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 integration module for Qt Designer

License:        LGPLv2+
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-designer-plugin-webkit

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdoctools-devel

# optional requirements
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kplotting-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kdewebkit-devel

Requires:       kf5-filesystem

%description
This framework provides plugins for Qt Designer that allow it to display
the widgets provided by various KDE frameworks, as well as a utility
(kgendesignerplugin) that can be used to generate other such plugins
from ini-style description files.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kdesignerplugin5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kdesignerplugin5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/kgendesignerplugin
%{_kf5_qtplugindir}/designer/*.so
%{_kf5_datadir}/kf5/widgets/*
%{_kf5_mandir}/man1/*
%{_kf5_mandir}/*/man1/*kgendesignerplugin.1.gz
%exclude %{_kf5_mandir}/man1

%files devel
%{_kf5_libdir}/cmake/KF5DesignerPlugin


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
