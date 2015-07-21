%global qt_module qtgraphicaleffects

Summary: Qt5 - QtGraphicalEffects component
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively from qt5-qtbase for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# debuginfo.list ends up empty/blank anyway, since the included qml is *basically* noarch
# todo: look into making this pkg proper noarch instead
%global debug_package %{nil}

BuildRequires: freedesktop-sdk-base

BuildRequires: qt5-qtbase-dev

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Graphical Effects module provides a set of QML types for adding
visually impressive and configurable effects to user interfaces. Effects
are visual items that can be added to Qt Quick user interface as UI
components.

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
%dir %{_qt5_archdatadir}/qml/
%{_qt5_archdatadir}/qml/QtGraphicalEffects/

%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtgraphicaleffects.qch
%{_qt5_docdir}/qtgraphicaleffects/


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
