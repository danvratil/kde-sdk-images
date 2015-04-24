%global framework kinit

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 tier 3 solution for process launching

License:        LGPLv2+ and BSD
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdoctools-devel

Requires:       kf5-filesystem

%description
kdeinit is a process launcher somewhat similar to the famous init used for
booting UNIX.

It launches processes by forking and then loading a dynamic library which should
contain a 'kdemain(...)' function.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kinit5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kinit5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/*
%{_kf5_libdir}/libkdeinit5_klauncher.so
%{_kf5_libexecdir}/*
%{_kf5_mandir}/man8/kdeinit5.8.gz
%{_kf5_mandir}/*/man8/kdeinit5.8.gz
%exclude %{_kf5_mandir}/man8

%files devel
%{_kf5_libdir}/cmake/KF5Init
%{_kf5_datadir}/dbus-1/interfaces/*.xml


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
