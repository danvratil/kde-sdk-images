Name:           kf5-platform
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Platform

License:        Various
BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires:  freedesktop-platform
BuildRequires:  qt5-platform

BuildRequires:  dbusmenu-qt5-dev
BuildRequires:  sgml-common
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  giflib-dev
BuildRequires:  ilmbase-dev
BuildRequires:  OpenEXR-dev
BuildRequires:  libupnp-dev

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-filesystem
BuildRequires:  kf5-rpm-macros

BuildRequires:  kf5-attica-dev
BuildRequires:  kf5-frameworkintegration-dev
BuildRequires:  kf5-kactivities-dev
BuildRequires:  kf5-kapidox
BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kauth-dev
BuildRequires:  kf5-kbookmarks-dev
BuildRequires:  kf5-kcmutils-dev
BuildRequires:  kf5-kcodecs-dev
BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kcrash-dev
BuildRequires:  kf5-kdbusaddons-dev
BuildRequires:  kf5-kdeclarative-dev
BuildRequires:  kf5-kded-dev
BuildRequires:  kf5-kdelibs4support-dev
BuildRequires:  kf5-kdesignerplugin-dev
BuildRequires:  kf5-kdesu-dev
BuildRequires:  kf5-kdewebkit-dev
BuildRequires:  kf5-kdnssd-dev
BuildRequires:  kf5-kdoctools-dev
BuildRequires:  kf5-kemoticons-dev
BuildRequires:  kf5-kglobalaccel-dev
BuildRequires:  kf5-kguiaddons-dev
BuildRequires:  kf5-khtml-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kidletime-dev
BuildRequires:  kf5-kimageformats
BuildRequires:  kf5-kinit-dev
BuildRequires:  kf5-kio-dev
BuildRequires:  kf5-kitemmodels-dev
BuildRequires:  kf5-kitemviews-dev
BuildRequires:  kf5-kjobwidgets-dev
BuildRequires:  kf5-kjsembed-dev
BuildRequires:  kf5-kjs-dev
BuildRequires:  kf5-kmediaplayer-dev
BuildRequires:  kf5-knewstuff-dev
BuildRequires:  kf5-knotifications-dev
BuildRequires:  kf5-knotifyconfig-dev
BuildRequires:  kf5-kpackage-dev
BuildRequires:  kf5-kparts-dev
BuildRequires:  kf5-kpeople-dev
BuildRequires:  kf5-kplotting-dev
BuildRequires:  kf5-kpty-dev
BuildRequires:  kf5-kross-dev
BuildRequires:  kf5-krunner-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-ktexteditor-dev
BuildRequires:  kf5-ktextwidgets-dev
BuildRequires:  kf5-kunitconversion-dev
BuildRequires:  kf5-kwallet-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-kxmlgui-dev
BuildRequires:  kf5-kxmlrpcclient-dev
#BuildRequires:  kf5-modemmanager-qt-dev
#BuildRequires:  kf5-networkmanager-qt-dev
BuildRequires:  kf5-plasma-dev
BuildRequires:  kf5-solid-dev
BuildRequires:  kf5-sonnet-dev
BuildRequires:  kf5-threadweaver-dev

BuildRequires:  breeze
BuildRequires:  oxygen-icon-theme

BuildRequires:  kio-extras

Requires:       freedesktop-platform
Requires:       qt5-platform

Requires:       dbusmenu-qt5
Requires:       xz
Requires:       ilmbase
Requires:       OpenEXR
Requires:       libupnp
Requires:       giflib

Requires:       extra-cmake-modules
Requires:       kf5-filesystem
Requires:       kf5-attica
Requires:       kf5-frameworkintegration
Requires:       kf5-kactivities
Requires:       kf5-kapidox
Requires:       kf5-karchive
Requires:       kf5-kauth
Requires:       kf5-kbookmarks
Requires:       kf5-kcmutils
Requires:       kf5-kcodecs
Requires:       kf5-kcompletion
Requires:       kf5-kconfig
Requires:       kf5-kconfigwidgets
Requires:       kf5-kcoreaddons
Requires:       kf5-kcrash
Requires:       kf5-kdbusaddons
Requires:       kf5-kdeclarative
Requires:       kf5-kded
Requires:       kf5-kdelibs4support
Requires:       kf5-kdesignerplugin
Requires:       kf5-kdesu
Requires:       kf5-kdewebkit
Requires:       kf5-kdnssd
Requires:       kf5-kdoctools
Requires:       kf5-kemoticons
Requires:       kf5-kglobalaccel
Requires:       kf5-kguiaddons
Requires:       kf5-khtml
Requires:       kf5-ki18n
Requires:       kf5-kiconthemes
Requires:       kf5-kidletime
Requires:       kf5-kimageformats
Requires:       kf5-kinit
Requires:       kf5-kio
Requires:       kf5-kitemmodels
Requires:       kf5-kitemviews
Requires:       kf5-kjobwidgets
Requires:       kf5-kjsembed
Requires:       kf5-kjs
Requires:       kf5-kmediaplayer
Requires:       kf5-knewstuff
Requires:       kf5-knotifications
Requires:       kf5-knotifyconfig
Requires:       kf5-kpackage
Requires:       kf5-kparts
Requires:       kf5-kpeople
Requires:       kf5-kplotting
Requires:       kf5-kpty
Requires:       kf5-kross
Requires:       kf5-krunner
Requires:       kf5-kservice
Requires:       kf5-ktexteditor
Requires:       kf5-ktextwidgets
Requires:       kf5-kunitconversion
Requires:       kf5-kwallet
Requires:       kf5-kwidgetsaddons
Requires:       kf5-kwindowsystem
Requires:       kf5-kxmlgui
Requires:       kf5-kxmlrpcclient
#Requires:       kf5-modemmanager-qt
#Requires:       kf5-networkmanager-qt
Requires:       kf5-plasma
Requires:       kf5-solid
Requires:       kf5-sonnet
Requires:       kf5-threadweaver

Requires:       breeze
Requires:       breeze-icon-theme
Requires:       oxygen-icon-theme

Requires:       kio-extras

%description
Meta package for KDE SDK dependencies

%prep

%build

%install

%files

%changelog
* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com>
- add kio-extras

* Wed May 06 2015 Daniel Vrátil <dvratil@redhat.com>
- add oxygen

* Tue May 05 2015 Daniel Vrátil <dvratil@redhat.com>
- add breeze

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com>
- Initial version
