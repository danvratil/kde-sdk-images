%global framework ktexteditor

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 with advanced embeddable text editor

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
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtxmlpatterns-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-sonnet-devel

%if 0%{?fedora} >= 22
BuildRequires:  libgit2-devel >= 0.22.0
%endif

Requires:       kf5-filesystem

%description
KTextEditor provides a powerful text editor component that you can embed in your
application, either as a KPart or using the KF5::TextEditor library (if you need
more control).

The text editor component contains many useful features, from syntax
highlighting and automatic indentation to advanced scripting support, making it
suitable for everything from a simple embedded text-file editor to an advanced
IDE.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kparts-devel

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
%find_lang ktexteditor5_qt --with-qt --all-name


%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :

%files -f ktexteditor5_qt.lang
%doc COPYING.LIB README.md
%config %{_sysconfdir}/xdg/kate*
%{_kf5_libdir}/libKF5TextEditor.so.*
%{_kf5_plugindir}/parts/katepart.so
%{_kf5_datadir}/kservices5/katepart.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/katepart5/script/
%{_kf5_datadir}/katepart5/syntax/
%{_kf5_datadir}/kxmlgui5/katepart/katepart5ui.rc

%files devel
%{_kf5_libdir}/libKF5TextEditor.so
%{_kf5_libdir}/cmake/KF5TextEditor
%{_kf5_includedir}/ktexteditor_version.h
%{_kf5_includedir}/KTextEditor
%{_kf5_archdatadir}/mkspecs/modules/qt_KTextEditor.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
