%global framework kcompletion

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 2 addon with auto completion widgets and classes

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

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kwidgetsaddons-devel

Requires:       kf5-filesystem

%description
KCompletion provides widgets with advanced completion support as well as a
lower-level completion class which can be used with your own widgets.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-devel
Requires:       kf5-kwidgetsaddons-devel

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
%find_lang kcompletion5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kcompletion5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5Completion.so.*

%files devel
%{_kf5_includedir}/kcompletion_version.h
%{_kf5_includedir}/KCompletion
%{_kf5_libdir}/libKF5Completion.so
%{_kf5_libdir}/cmake/KF5Completion
%{_kf5_archdatadir}/mkspecs/modules/qt_KCompletion.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
