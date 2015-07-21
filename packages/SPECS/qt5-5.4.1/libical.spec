Summary:	Reference implementation of the iCalendar data type and serialization format
Name:		libical
Version:	1.0.1
Release:	1%{?dist}
License:	LGPLv2 or MPLv1.1
URL:		http://freeassociation.sourceforge.net/
Source:		https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		libical-1.0-avoid-putenv.patch

BuildRequires: qt5-sdk-base

%description
Reference implementation of the iCalendar data type and serialization format
used in dozens of calendaring and scheduling products.

%package dev
Summary:	Development files for libical
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description dev
The libical-devel package contains libraries and header files for developing
applications that use libical.

%prep
%setup -q
%patch0 -p1 -b .avoid-putenv

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# omit static libs
rm -fv %{buildroot}%{_libdir}/lib*.a

%check
make test ARGS="-V" -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE ReadMe.txt THANKS
%{_libdir}/libical.so.1*
%{_libdir}/libicalss.so.1*
%{_libdir}/libicalvcal.so.1*

%files dev
%doc doc/UsingLibical.txt
%{_includedir}/ical.h
%{_libdir}/libical.so
%{_libdir}/libicalss.so
%{_libdir}/libicalvcal.so
%{_libdir}/pkgconfig/libical.pc
%{_libdir}/cmake/LibIcal/
%{_includedir}/libical/

%changelog
* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.1-1
- Initial version (forked from Fedora)
