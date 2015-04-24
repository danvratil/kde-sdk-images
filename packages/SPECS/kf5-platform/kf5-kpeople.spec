%global framework kpeople

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 library for contact and people aggregation

License:        LGPLv2+
URL:            https://projects.kde.org/projects/frameworks/kpeople

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

# use non-conflicting libkpeople5 translation catalog
Patch1: kpeople-catalog.patch

## Once ktp-kf5 stack is ready, can consider Obsoletes
#Obsoletes: libkpeople < 1.0

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kitemviews-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 library for interaction with XML RPC services.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
## enable when ktp-kf5 stack is updated
#Obsoletes:      libkpeople-devel < 1.0

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%patch1 -p1 -b .catalog

for po in po/*/libkpeople.po ; do
pushd $(dirname $po)
mv libkpeople.po libkpeople5.po
popd
done


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
    -DENABLE_EXAMPLES:BOOL=OFF
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kpeople5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kpeople5_qt.lang
%doc COPYING
%{_kf5_libdir}/libKF5People.so.*
%{_kf5_libdir}/libKF5PeopleWidgets.so.*
%{_kf5_libdir}/libKF5PeopleBackend.so.*
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_qmldir}/org/kde/people

%files devel
%{_kf5_includedir}/KPeople
%{_kf5_libdir}/libKF5People.so
%{_kf5_libdir}/libKF5PeopleWidgets.so
%{_kf5_libdir}/libKF5PeopleBackend.so
%{_kf5_libdir}/cmake/KF5People
%{_kf5_datadir}/kf5/kpeople
%{_kf5_archdatadir}/mkspecs/modules/qt_KPeople.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KPeopleWidgets.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
