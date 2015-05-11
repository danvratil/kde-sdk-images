Name:           breeze
Version:        5.3.0
Release:        2%{?dist}
Summary:        Artwork, styles and assets for the Breeze visual style for the Plasma Desktop

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/breeze

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

Source10:       breeze-metadata.desktop
Source11:       breeze-defaults

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtx11extras-dev

BuildRequires:	kf5-kservice-dev
BuildRequires:  kf5-kcmutils-dev

BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kcompletion-dev
BuildRequires:  kf5-frameworkintegration-dev
BuildRequires:  kf5-kwindowsystem-dev

BuildRequires:  libxcb-dev

BuildRequires:  gettext

Requires:       kf5-filesystem

Requires:       %{name}-common = %{version}-%{release}

%description
%{summary}.

%package        common
Summary:        Common files shared between KDE 4 and Plasma 5 versions of the Breeze style
BuildArch:      noarch
%description    common
%{summary}.

%package -n     breeze-icon-theme
Summary:        Breeze icon theme
BuildArch:      noarch
%description -n breeze-icon-theme
%{summary}.

%prep
%setup -n %{name}-%{version}


%build
# We don't need window decorations in sandboxes
sed -i "s/add_subdirectory(kdecoration)/#add_subdirectory(kdecoration)/g" CMakeLists.txt

mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang breeze --with-qt --all-name

# Install breeze look-and-feel metadata so that frameworkintegration
# plugin picks it up otherwise it falls back to Oxygen
mkdir -p %{buildroot}/%{_datadir}/plasma/look-and-feel/org.kde.breeze.desktop/contents
install %{SOURCE10} %{buildroot}%{_datadir}/plasma/look-and-feel/org.kde.breeze.desktop/metadata.desktop
install %{SOURCE11} %{buildroot}%{_datadir}/plasma/look-and-feel/org.kde.breeze.desktop/contents/defaults


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files
%doc cursors/Breeze/README COPYING COPYING-ICONS
%{_kf5_qtplugindir}/styles/breeze.so
%{_kf5_datadir}/kstyle/themes/breeze.themerc
%{_kf5_qtplugindir}/kstyle_breeze_config.so
%{_kf5_datadir}/kconf_update/kde4breeze.upd
%{_kf5_libdir}/kconf_update_bin/kde4breeze
%{_kf5_datadir}/kconf_update/gtkbreeze.upd
%{_kf5_libdir}/kconf_update_bin/gtkbreeze
%{_kf5_qmldir}/QtQuick/Controls/Styles/Breeze
%{_bindir}/breeze-settings5
%{_datadir}/icons/hicolor/scalable/apps/breeze-settings.svgz
%{_kf5_datadir}/kservices5/breezestyleconfig.desktop
%{_kf5_datadir}/plasma/look-and-feel/org.kde.breeze.desktop

%files common -f breeze.lang
%{_datadir}/color-schemes/*.colors
%{_datadir}/QtCurve/Breeze.qtcurve
%{_datadir}/wallpapers/Next

%post -n breeze-icon-theme
touch --no-create %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :

%posttrans -n breeze-icon-theme
gtk-update-icon-cache %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :

%postun -n breeze-icon-theme
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :
fi

%files -n breeze-icon-theme
%{_datadir}/icons/breeze_cursors
%{_datadir}/icons/breeze
%{_datadir}/icons/breeze-dark
%{_datadir}/icons/Breeze_Snow

%changelog
* Wed May 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- add look-and-feel metadata

* Tue May 05 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Initial version (forked from Fedora)
