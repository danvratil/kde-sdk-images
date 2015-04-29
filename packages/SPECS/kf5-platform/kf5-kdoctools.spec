%global framework kdoctools

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 2 addon for generating documentation

License:        GPLv2+ and MIT
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-dev
BuildRequires:  kf5-ki18n-dev
BuildRequires:  kf5-karchive-dev

Requires:       docbook-dtds
Requires:       docbook-style-xsl
Requires:       kf5-filesystem

%description
Provides tools to generate documentation in various format from DocBook files.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       kf5-kdoctools-static = %{version}-%{release}
Requires:       qt5-qtbase-dev
Requires:       kf5-karchive-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        User documentation and help for %{name}
Requires:       kf5-filesystem
%description    doc
Documentation and user help for %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
# Get rid of Perl dependencies. It's impossible to get it work
# in this lousy runtime
echo -e "function(kdoctools_encode_uri _original_uri)\nendfunction()" > cmake/uriencode.cmake


mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kdoctools5_qt --with-qt --with-man --with-kde --all-name


%files -f kdoctools5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/checkXML5
%{_kf5_bindir}/meinproc5
%{_kf5_datadir}/man/man1/*
%{_kf5_datadir}/man/man7/*
%{_kf5_datadir}/man/man8/*
%{_kf5_datadir}/kf5/kdoctools

%files dev
%{_kf5_includedir}/XsltKde
%{_kf5_libdir}/libKF5XsltKde.a
%{_kf5_libdir}/cmake/KF5DocTools

%files doc
%{_kf5_docdir}/HTML/*/kdoctools5-common


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
