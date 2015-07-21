%global qt_module qttranslations

Summary: Qt5 - QtTranslations module
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

License: LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
Url:     http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildArch: noarch

BuildRequires: freedesktop-sdk-base
BuildRequires: qt5-qttools-dev

%description
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{qmake_qt5}
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

%find_lang %{name} --all-name --with-qt --without-mo


%files -f %{name}.lang
%doc LICENSE.LGPL* LGPL_EXCEPTION.txt


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
