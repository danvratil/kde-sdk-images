Name:           qt5-platform
Version:        0.1
Release:        1%{?dist}
Summary:        Qt 5 Platform

License:        Various
BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires:  freedesktop-platform

BuildRequires:  qt5-qtbase-dev
#BuildRequires:  qt5-qtconnectivity-dev
BuildRequires:  qt5-qtdeclarative-dev
BuildRequires:  qt5-qtgraphicaleffects
BuildRequires:  qt5-qtquickcontrols
BuildRequires:  qt5-qtimageformats
BuildRequires:  qt5-qtlocation-dev
BuildRequires:  qt5-qtmultimedia-dev
BuildRequires:  qt5-qtquick1-dev
BuildRequires:  qt5-qtscript-dev
BuildRequires:  qt5-qtsensors-dev
BuildRequires:  qt5-qtserialport-dev
BuildRequires:  qt5-qtsvg-dev
BuildRequires:  qt5-qttools-dev
BuildRequires:  qt5-qttranslations
#BuildRequires:  qt5-qtwayland-dev
BuildRequires:  qt5-qtwebkit-dev
BuildRequires:  qt5-qtx11extras-dev
BuildRequires:  qt5-qtxmlpatterns-dev
BuildRequires:  phonon-dev


Requires:       freedesktop-platform

Requires:       glx-utils

Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
# TODO: DB backends?
#Requires:       qt5-qtbase-mysql
#Requires:       qt5-qtbase-postgresql
#Requires:       qt5-qtconnectivity
Requires:       qt5-qtdeclarative
Requires:       qt5-designer-plugin-webkit
Requires:       qt5-qtgraphicaleffects
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtimageformats
Requires:       qt5-qtlocation
Requires:       qt5-qtmultimedia
Requires:       qt5-qtquick1
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtscript
Requires:       qt5-qtsensors
Requires:       qt5-qtserialport
Requires:       qt5-qtsvg
Requires:       qt5-qttools
Requires:       qt5-qttools-static
Requires:       qt5-qttools-libs-clucene
Requires:       qt5-qttranslations
#Requires:       qt5-qtwayland
Requires:       qt5-qtwebkit
Requires:       qt5-qtx11extras
Requires:       qt5-qtxmlpatterns
Requires:       phonon
Requires:       phonon-backend-gstreamer


%description
Meta package for KDE SDK dependencies

%prep

%build

%install

%files

%changelog
* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com>
- Initial version
