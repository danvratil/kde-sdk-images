Name:           oxygen-icon-theme
Summary:        Oxygen icon theme
Version:        15.04.0
Release:        1%{?dist}

# http://techbase.kde.org/Policies/Licensing_Policy
License:        LGPLv3+
URL:            http://www.kde.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/oxygen-icons-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  extra-cmake-modules
BuildRequires:  cmake

%description
%{summary}.


%prep
%setup -q -n oxygen-icons-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# FIXME: We totally need to enable this, but for now there's no hardlink

# As of 4.12.3, hardlink reports
#Directories 78
#Objects 6926
#IFREG 6848
#Mmaps 902
#Comparisons 902
#Linked 902
#saved 8339456
#/usr/sbin/hardlink -c -v %{buildroot}%{_datadir}/icons/oxygen

# create/own all potential dirs
mkdir -p %{buildroot}%{_datadir}/icons/oxygen/{16x16,22x22,24x24,32x32,36x36,48x48,64x64,96x96,128x128,512x512,scalable}/{actions,apps,devices,mimetypes,places}

# %%ghost icon.cache
touch  %{buildroot}%{_datadir}/icons/oxygen/icon-theme.cache


%post
touch --no-create %{_datadir}/icons/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/oxygen &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/oxygen &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/oxygen &> /dev/null || :
fi

%files
%doc AUTHORS CONTRIBUTING COPYING
%dir %{_datadir}/icons/oxygen/
%ghost %{_datadir}/icons/oxygen/icon-theme.cache
%{_datadir}/icons/oxygen/index.theme
%{_datadir}/icons/oxygen/*x*/
%{_datadir}/icons/oxygen/scalable/


%changelog
* Wed May 06 2015 Daniel Vrátil <dvratil@redhat.com> - 15.04.0-1
- Initial version (forked from Fedora)
