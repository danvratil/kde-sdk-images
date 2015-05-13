Name:           kio-extras
Version:        5.3.0
Release:        1%{?dist}
Summary:        Additional components to increase the functionality of KIO Framework

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kio-extras


%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

## downstream patches
# temporarily adjust translation catalog until kio_mtp updates hit stable
#Patch1: kio-extras-5.2.2-mtp_catalog.patch

BuildRequires:  kf5-rpm-macros

BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtsvg-dev

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-karchive-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-kcoreaddons-dev
BuildRequires:  kf5-kdbusaddons-dev
BuildRequires:  kf5-kdoctools-dev
BuildRequires:  kf5-kdnssd-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kio-dev >= 5.3.0-1
BuildRequires:  kf5-khtml-dev
BuildRequires:  kf5-kdelibs4support-dev
BuildRequires:  kf5-solid-dev
BuildRequires:  kf5-kpty-dev

BuildRequires:  phonon-dev

#BuildRequires:  openslp-devel
#BuildRequires:  libmtp-devel
#BuildRequires:  libsmbclient-devel
#BuildRequires:  libssh-devel
#BuildRequires:  bzip2-devel
#BuildRequires:  exiv2-devel
#BuildRequires:  OpenEXR-devel
#BuildRequires:  libjpeg-devel
#BuildRequires:  lzma-devel

Requires:       kf5-filesystem

# short-lived subpkg, locale conflicts fixed in kio_mtp instead
#Obsoletes:      kio-extras-mtp-common < 5.2.2-3

%description
%{summary}.

%package        docs
Summary:        Documentation and user manuals for %{name}
#Obsoletes:      kde-runtime-docs < 5.0.0-1
# when went noarch
#Obsoletes:      kio-extras-doc < 5.8.0-2
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%description    docs
%{summary}.


%prep
%setup -q -n %{name}-%{version}

# temporary
#%patch1 -p1 -b .mtp_catalog
#for po in po/*/kio_mtp.po ; do
#pushd $(dirname $po)
#mv kio_mtp.po kio_mtp5.po
#popd
#done


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --all-name --with-qt


%post
/sbin/ldconfig
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f %{name}.lang
%{_libdir}/libmolletnetwork5.so.*
%{_kf5_plugindir}/kio/archive.so
%{_kf5_plugindir}/kio/bookmarks.so
%{_kf5_plugindir}/kio/desktop.so
%{_kf5_plugindir}/kio/filenamesearch.so
%{_kf5_plugindir}/kio/filter.so
%{_kf5_plugindir}/kio/fish.so
%{_kf5_plugindir}/kio/info.so
%{_kf5_plugindir}/kio/man.so
#%{_kf5_plugindir}/kio/mtp.so
%{_kf5_plugindir}/kio/network.so
%{_kf5_plugindir}/kio/nfs.so
%{_kf5_plugindir}/kio/recentdocuments.so
%{_kf5_plugindir}/kio/settings.so
#%{_kf5_plugindir}/kio/sftp.so
#%{_kf5_plugindir}/kio/smb.so
%{_kf5_plugindir}/kio/thumbnail.so
%{_kf5_qtplugindir}/kio_about.so
%{_kf5_qtplugindir}/kfileaudiopreview.so
%{_kf5_qtplugindir}/comicbookthumbnail.so
%{_kf5_qtplugindir}/imagethumbnail.so
%{_kf5_qtplugindir}/jpegthumbnail.so
%{_kf5_qtplugindir}/kded_desktopnotifier.so
%{_kf5_qtplugindir}/kded_networkwatcher.so
%{_kf5_qtplugindir}/kded_recentdocumentsnotifier.so
%{_kf5_qtplugindir}/libkmanpart.so
%{_kf5_qtplugindir}/svgthumbnail.so
%{_kf5_qtplugindir}/textthumbnail.so
%{_datadir}/kio_desktop/
%{_datadir}/kio_docfilter/
%{_datadir}/kio_bookmarks/
%{_datadir}/kio_info/
%dir %{_datadir}/konqsidebartng/
%dir %{_datadir}/konqsidebartng/virtual_folders/
%dir %{_datadir}/konqsidebartng/virtual_folders/remote/
%{_datadir}/konqsidebartng/virtual_folders/remote/virtualfolder_network.desktop
#%dir %{_datadir}/konqueror/
#%dir %{_datadir}/konqueror/dirtree/
#%dir %{_datadir}/konqueror/dirtree/remote/
#%{_datadir}/konqueror/dirtree/remote/mtp-network.desktop
#%{_datadir}/konqueror/dirtree/remote/smb-network.desktop
%{_datadir}/remoteview/
#%{_kf5_datadir}/solid/actions/solid_mtp.desktop
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/thumbcreator.desktop
%{_datadir}/dbus-1/interfaces/kf5_org.kde.network.kioslavenotifier.xml
%{_datadir}/mime/packages/kf5_network.xml
%{_datadir}/config.kcfg/jpegcreatorsettings5.kcfg

%files docs
# FIXME %lang() support!!!!
%{_docdir}/HTML/*/kioslave5/
%{_docdir}/HTML/*/kcontrol/
#%lang(pt_BR) %{_docdir}/HTML/pt_BR/kcontrol/


%changelog
* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Initial version (forked from Fedora)
