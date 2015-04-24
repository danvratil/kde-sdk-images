Summary: Gstreamer phonon backend
Name:    phonon-backend-gstreamer
Version: 4.8.2
Release: 1%{?dist}

License: LGPLv2+
URL:     http://phonon.kde.org/
Source0: http://download.kde.org/stable/phonon/phonon-backend-gstreamer/%{version}/src/phonon-backend-gstreamer-%{version}.tar.xz


BuildRequires: qt5-sdk-base
BuildRequires: phonon-dev
BuildRequires: qt5-qtbase-dev

BuildRequires: gstreamer1-dev
BuildRequires: gstreamer1-plugins-base-dev

# not *strictly* required, but strongly recommended by upstream when built
# with USE_INSTALL_PLUGIN
#Requires: PackageKit-gstreamer-plugin
#Requires: phonon%{?_isa} => %{phonon_version}

%description
%{summary}.

%prep
%setup -q -n phonon-backend-gstreamer-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DUSE_INSTALL_PLUGIN:BOOL=ON \
  -DPHONON_BUILD_PHONON4QT5:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:

%files
%doc COPYING.LIB
%{_qt5_plugindir}/phonon4qt5_backend/phonon_gstreamer.so
%{_datadir}/icons/hicolor/*/*/phonon-gstreamer.*

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 4.8.2-1
- Initial version (forked from Fedora)
