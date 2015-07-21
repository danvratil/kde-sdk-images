%global framework kauth

# no systemd -> no polkit -> no plkit-qt5 - use dummy backend
%define build_polkit 0

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 2 integration module to perform actions as privileged user

License:        LGPLv2+
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

%if 0%{?build_polkit}
BuildRequires:  polkit-qt5-1-dev
%endif

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qttools-dev

BuildRequires:  kf5-kcoreaddons-dev

Requires:       kf5-filesystem

%description
KAuth is a framework to let applications perform actions as a privileged user.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcoreaddons-dev
%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
# Remove once 9be07165 is fixed/explained
%{cmake_kf5} .. -DLIBEXEC_INSTALL_DIR=%{_kf5_libexecdir}
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kauth5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kauth5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5Auth.so.5*
%{_kf5_sysconfdir}/dbus-1/system.d/org.kde.kf5auth.conf
%{_kf5_qtplugindir}/kauth/
%{_kf5_datadir}/kf5/kauth/
%if 0%{?build_polkit}
%{_kf5_libexecdir}/kauth/kauth-policy-gen
%endif

%files dev
%{_kf5_includedir}/kauth_version.h
%{_kf5_includedir}/KAuth/
%{_kf5_libdir}/libKF5Auth.so
%{_kf5_libdir}/cmake/KF5Auth/
%{_kf5_archdatadir}/mkspecs/modules/qt_KAuth.pri


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
