%global framework kitemviews

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon with item views

License:        GPLv2+ and LGPLv2+
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

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 1 addon with item views.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel

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
%make_install -C %{_target_platform}
%find_lang kitemviews5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kitemviews5_qt.lang
%doc COPYING COPYING.LIB README.md
%{_kf5_libdir}/libKF5ItemViews.so.*

%files devel
%doc
%{_kf5_includedir}/kitemviews_version.h
%{_kf5_includedir}/KItemViews
%{_kf5_libdir}/libKF5ItemViews.so
%{_kf5_libdir}/cmake/KF5ItemViews
%{_kf5_archdatadir}/mkspecs/modules/qt_KItemViews.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
