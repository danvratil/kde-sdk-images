Name:           qt5-sdk
Version:        5.4.1
Release:        1%{?dist}
Summary:        Qt 5 sdk
Source1:        rpm-macros

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires:  qt5-platform
BuildRequires:  freedesktop-sdk

Requires:       qt5-platform
Requires:       freedesktop-sdk

Requires:       alsa-lib-dev
Requires:       at-spi2-core-dev
Requires:       clucene-core-dev
Requires:       glew-dev
Requires:       libmng-dev
Requires:       mesa-libGLU-dev
Requires:       openal-soft-dev
Requires:       pcre16-dev
Requires:       pcre32-dev
Requires:       portaudio-dev
Requires:       xcb-util-dev
Requires:       xcb-util-image-dev
Requires:       xcb-util-keysyms-dev
Requires:       xcb-util-renderutil-dev
Requires:       xcb-util-wm-dev

Requires:       qt5-qtbase-dev
Requires:       qt5-qtbase-static
#Requires:       qt5-qtconnectivity-dev
Requires:       qt5-qtdeclarative-dev
Requires:       qt5-qtdeclarative-static
Requires:       qt5-qtgraphicaleffects
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtimageformats
Requires:       qt5-qtlocation-dev
Requires:       qt5-qtmultimedia-dev
Requires:       qt5-qtquick1-dev
Requires:       qt5-qtscript-dev
Requires:       qt5-qtsensors-dev
Requires:       qt5-qtserialport-dev
Requires:       qt5-qtsvg-dev
Requires:       qt5-qttools-dev
Requires:       qt5-qttools-static
Requires:       qt5-qttranslations
#Requires:      qt5-qtwayland-dev
Requires:       qt5-qtwebkit-dev
Requires:       qt5-qtx11extras-dev
Requires:       qt5-qtxmlpatterns-dev

Requires:       phonon-dev

%description
Meta package for Qt 5 SDK dependencies

%prep


%build

%files

%changelog
* Mon Apr 20 2015 Daniel Vrátil <dvratil@redhat.com>
- Initial version
