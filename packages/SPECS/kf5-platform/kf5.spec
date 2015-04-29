Name:           kf5
Version:        5.9.0
Release:        1%{?dist}
Summary:        Filesystem and RPM macros for KDE Frameworks 5
License:        BSD
BuildArch:      noarch
URL:            http://www.kde.org

Source0:        macros.kf5

Requires:       kf5-filesystem
Requires:       kf5-rpm-macros

%description
Filesystem and RPM macros for KDE Frameworks 5

%package        filesystem
Summary:        Filesystem for KDE Frameworks 5
%description    filesystem
Filesystem for KDE Frameworks 5.

%package        rpm-macros
Summary:        RPM macros for KDE Frameworks 5
%description    rpm-macros
RPM macros for building KDE Frameworks 5 packages.


%install
# See macros.kf5 where the directories are specified
mkdir -p %{buildroot}%{_prefix}/lib/qt5/plugins/kf5
mkdir -p %{buildroot}%{_prefix}/lib64/qt5/plugins/kf5
mkdir -p %{buildroot}%{_includedir}/KF5
mkdir -p %{buildroot}%{_libexecdir}/kf5
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/{env,shutdown}

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
install -pm644 %{_sourcedir}/macros.kf5 %{buildroot}%{_rpmconfigdir}/macros.d

%files
# Empty package

%files filesystem
%{_sysconfdir}/xdg/plasma-workspace/
%{_prefix}/lib/qt5/plugins/kf5
%{_prefix}/lib64/qt5/plugins/kf5
%{_includedir}/KF5
%{_libexecdir}/kf5


%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.kf5


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
