
%global qt_module qttranslations

Summary: Qt5 - QtTranslations module
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

License: LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
Url:     http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.4/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildArch: noarch

BuildRequires: qt5-qttools-devel >= %{version}

%description
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
qmake-qt5
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

%find_lang %{name} --all-name --with-qt --without-mo


%files -f %{name}.lang
%doc LICENSE.LGPL* LGPL_EXCEPTION.txt


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
