Version: 1.6.19
Summary: Universal Plug and Play (UPnP) SDK
Name: libupnp
Release: 1%{?dist}
License: BSD
Group: System Environment/Libraries
URL: http://www.libupnp.org/
Source: http://downloads.sourceforge.net/pupnp/%{name}-%{version}.tar.bz2

%define docdeveldir %{_docdir}/%{name}-dev-%{version}
%define docdir %{_docdir}/%{name}-%{version}

%description
The Universal Plug and Play (UPnP) SDK for Linux provides 
support for building UPnP-compliant control points, devices, 
and bridges on Linux.

%package dev
Group: Development/Libraries
Summary: Include files needed for development with libupnp
Requires: libupnp = %{version}-%{release}

%description dev
The libupnp-dev package contains the files necessary for development with
the UPnP SDK libraries.

%prep
%setup -q

%build
%configure --enable-static=no --enable-ipv6
make %{?_smp_mflags}

%install
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%{__rm} %{buildroot}%{_libdir}/{libixml.la,libthreadutil.la,libupnp.la}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE THANKS
%{_libdir}/libixml.so.2*
%{_libdir}/libthreadutil.so.6*
%{_libdir}/libupnp.so.6*

%files dev
%defattr(0644,root,root,0755)
#doc _devel_docs/*
%{_includedir}/upnp/
%{_libdir}/libixml.so
%{_libdir}/libthreadutil.so
%{_libdir}/libupnp.so
%{_libdir}/pkgconfig/libupnp.pc

%clean
rm -rf %{buildroot}

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 1.6.19-1
- Initial version (forked from Fedora)

