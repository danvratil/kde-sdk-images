
Name:	 OpenEXR
Summary: A high dynamic-range (HDR) image file format
Version: 2.2.0
Release: 1%{?dist}

License: BSD
URL:	 http://www.openexr.com/
Source0: http://download.savannah.nongnu.org/releases/openexr/openexr-%{version}.tar.gz

Obsoletes: openexr < %{version}-%{release}
Provides:  openexr = %{version}-%{release}

# https://github.com/openexr/openexr/issues/130
BuildConflicts: OpenEXR-dev < 2.2.0

BuildRequires: ilmbase-dev
BuildRequires: zlib-dev

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial
Light & Magic for use in computer imaging applications. This package contains
libraries and sample applications for handling the format.

%package dev
Summary: Headers and libraries for building apps that use %{name} 
Obsoletes: openexr-dev < %{version}-%{release}
Provides:  openexr-dev = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ilmbase-dev
%description dev
%{summary}.

%package libs
Summary: %{name} runtime libraries
%description libs
%{summary}.


%prep
%setup -q -n openexr-%{version}


%build
%configure --disable-static

# hack to omit unused-direct-shlib-dependencies
#sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

#unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion OpenEXR)" = "%{version}"
make %{?_smp_mflags} check ||:


%files
%{_bindir}/exr*

%post libs -p /sbin/ldconfig
%postun libs  -p /sbin/ldconfig

%files libs
%doc AUTHORS ChangeLog LICENSE NEWS README
%{_libdir}/libIlmImf-2_2.so.22*
%{_libdir}/libIlmImfUtil-2_2.so.22*

%files dev
#omit for now, they're mostly useless, and include multilib conflicts (#342781)
#doc rpmdocs/examples 
%{_datadir}/aclocal/openexr.m4
%{_includedir}/OpenEXR/*
%{_libdir}/libIlmImf*.so
%{_libdir}/pkgconfig/OpenEXR.pc


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 2.2.0-1
- Initial version (forked from Fedora)

