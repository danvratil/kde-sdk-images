%global framework kxmlgui

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for user-configurable main windows

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

BuildRequires:  libX11-dev

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev

BuildRequires:  kf5-kitemviews-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kglobalaccel-dev
BuildRequires:  kf5-kconfigwidgets-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-ktextwidgets-dev
BuildRequires:  kf5-kwidgetsaddons-dev
BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-attica-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for user-configurable main windows.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-dev
Requires:       kf5-kconfigwidgets-dev
Requires:       kf5-kglobalaccel-dev
Requires:       kf5-kiconthemes-dev
Requires:       kf5-kitemviews-dev
Requires:       kf5-ktextwidgets-dev
Requires:       kf5-kwindowsystem-dev
Requires:       qt5-qtbase-dev
Requires:       kf5-attica-dev

%description    dev
The %{name}-dev package contains libraries and header files for
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
%find_lang kxmlgui5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kxmlgui5_qt.lang
%doc COPYING COPYING.LIB README.md
%config %{_kf5_sysconfdir}/xdg/ui/ui_standards.rc
%{_kf5_libdir}/libKF5XmlGui.so.*
%{_kf5_libexecdir}/ksendbugmail
%{_kf5_datadir}/kf5/kxmlgui/

%files dev
%{_kf5_includedir}/kxmlgui_version.h
%{_kf5_includedir}/KXmlGui
%{_kf5_libdir}/libKF5XmlGui.so
%{_kf5_libdir}/cmake/KF5XmlGui
%{_kf5_archdatadir}/mkspecs/modules/qt_KXmlGui.pri


%changelog
* Tue Jul 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- Update to KF5 5.12

* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
