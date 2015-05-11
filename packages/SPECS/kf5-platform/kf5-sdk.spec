Name:           kf5-sdk
Version:        0.1
Release:        1%{?dist}
Summary:        KDE Frameworks 5 SDK

License:        Various
BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires:  kf5-platform
BuildRequires:  qt5-sdk

Requires:       kf5-platform
Requires:       qt5-sdk

Requires:       dbusmenu-qt5-dev
Requires:       sgml-common
Requires:       docbook-dtds
Requires:       docbook-style-xsl
Requires:       giflib-dev
Requires:       ilmbase-dev
Requires:       OpenEXR-dev
Requires:       libupnp-dev

Requires:       extra-cmake-modules
Requires:       kf5-filesystem
Requires:       kf5-rpm-macros

Requires:       kf5-attica-dev
Requires:       kf5-frameworkintegration-dev
Requires:       kf5-kactivities-dev
Requires:       kf5-kapidox
Requires:       kf5-karchive-dev
Requires:       kf5-kauth-dev
Requires:       kf5-kbookmarks-dev
Requires:       kf5-kcmutils-dev
Requires:       kf5-kcodecs-dev
Requires:       kf5-kcompletion-dev
Requires:       kf5-kconfig-dev
Requires:       kf5-kconfigwidgets-dev
Requires:       kf5-kcoreaddons-dev
Requires:       kf5-kcrash-dev
Requires:       kf5-kdbusaddons-dev
Requires:       kf5-kdeclarative-dev
Requires:       kf5-kded-dev
Requires:       kf5-kdelibs4support-dev
Requires:       kf5-kdesignerplugin-dev
Requires:       kf5-kdesu-dev
Requires:       kf5-kdewebkit-dev
Requires:       kf5-kdnssd-dev
Requires:       kf5-kdoctools-dev
Requires:       kf5-kemoticons-dev
Requires:       kf5-kglobalaccel-dev
Requires:       kf5-kguiaddons-dev
Requires:       kf5-khtml-dev
Requires:       kf5-ki18n-dev
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kidletime-dev
Requires:       kf5-kimageformats
Requires:       kf5-kinit-dev
Requires:       kf5-kio-dev
Requires:       kf5-kitemmodels-dev
Requires:       kf5-kitemviews-dev
Requires:       kf5-kjobwidgets-dev
Requires:       kf5-kjsembed-dev
Requires:       kf5-kjs-dev
Requires:       kf5-kmediaplayer-dev
Requires:       kf5-knewstuff-dev
Requires:       kf5-knotifications-dev
Requires:       kf5-knotifyconfig-dev
Requires:       kf5-kpackage-dev
Requires:       kf5-kparts-dev
Requires:       kf5-kpeople-dev
Requires:       kf5-kplotting-dev
Requires:       kf5-kpty-dev
Requires:       kf5-kross-dev
Requires:       kf5-krunner-dev
Requires:       kf5-kservice-dev
Requires:       kf5-ktexteditor-dev
Requires:       kf5-ktextwidgets-dev
Requires:       kf5-kunitconversion-dev
Requires:       kf5-kwallet-dev
Requires:       kf5-kwidgetsaddons-dev
Requires:       kf5-kwindowsystem-dev
Requires:       kf5-kxmlgui-dev
Requires:       kf5-kxmlrpcclient-dev
#Requires:       kf5-modemmanager-qt-dev
#Requires:       kf5-networkmanager-qt-dev
Requires:       kf5-plasma-dev
Requires:       kf5-solid-dev
Requires:       kf5-sonnet-dev
Requires:       kf5-threadweaver-dev

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
