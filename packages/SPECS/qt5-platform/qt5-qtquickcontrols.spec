%global qt_module qtquickcontrols

Name:           qt5-%{qt_module}
Version:        5.4.1
Summary:        Qt5 - module with set of QtQuick controls
Release:        1%{?dist}
License:        BSD and (LGPLv2 with exceptions or GPLv3 with exceptions) and GFDL
Url:            http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires:  freedesktop-sdk-base
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtdeclarative-dev

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Quick Controls module provides a set of controls that can be used to
build complete interfaces in Qt Quick.


%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{_qt5_qmake}
make %{?_smp_mflags}
make %{?_smp_mflags} docs


%install
make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

%files
# better to own this elsewhere? qt5-qtbase? -- rex
%dir %{_qt5_archdatadir}/qml
%{_qt5_archdatadir}/qml/QtQuick/
%{_qt5_prefix}/examples/quick/dialogs/systemdialogs
%doc LICENSE.FDL
%doc LICENSE.GPLv2
%doc LICENSE.LGPLv21
%doc LICENSE.LGPLv3
%doc LGPL_EXCEPTION.txt
%doc header.BSD

%files doc
%{_qt5_docdir}/qtquickcontrols.qch
%{_qt5_docdir}/qtquickcontrols/
%{_qt5_docdir}/qtquicklayouts.qch
%{_qt5_docdir}/qtquicklayouts/
%{_qt5_docdir}/qtquickdialogs.qch
%{_qt5_docdir}/qtquickdialogs/


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)

