
%global qt_module qtquickcontrols

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

Name:           qt5-%{qt_module}
Version:        5.4.1
Summary:        Qt5 - module with set of QtQuick controls
Release:        1%{?dist}
License:        BSD and (LGPLv2 with exceptions or GPLv3 with exceptions) and GFDL
Url:            http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  qt5-qtbase-static >= %{version}
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Core)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Quick Controls module provides a set of controls that can be used to
build complete interfaces in Qt Quick.


%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch

%description doc
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{_qt5_qmake}
make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif


%files
# better to own this elsewhere? qt5-qtbase? -- rex
%dir %{_qt5_archdatadir}/qml
%{_qt5_archdatadir}/qml/QtQuick/
%doc LICENSE.FDL
%doc LICENSE.LGPL
%doc LICENSE.GPL
%doc LGPL_EXCEPTION.txt
%doc header.BSD

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtquickcontrols.qch
%{_qt5_docdir}/qtquickcontrols/
%{_qt5_docdir}/qtquicklayouts.qch
%{_qt5_docdir}/qtquicklayouts/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)

