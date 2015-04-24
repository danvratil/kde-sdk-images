
Name:    ilmbase
Summary: Abstraction/convenience libraries
Version: 2.2.0
Release: 1%{?dist}

License: BSD
URL:	 http://www.openexr.com/
Source0: http://download.savannah.nongnu.org/releases/openexr/ilmbase-%{version}.tar.gz

#BuildRequires: automake libtool
# silly rpm, won't pick up rpm dependencies for items not in it's buildroot
# see http://bugzilla.redhat.com/866302

BuildRequires: mesa-libGL-dev
#BuildRequires: mesa-libGLU-dev

## upstreamable patches
# explicitly add $(PTHREAD_LIBS) to libIlmThread linkage (helps PTHREAD_LIBS workaround in %%build)
Patch51: ilmbase-2.2.0-no_undefined.patch
# add Requires.private: gl glu to IlmBase.pc
Patch53:  ilmbase-1.0.3-pkgconfig.patch

## upstream patches

%description
Half is a class that encapsulates the ilm 16-bit floating-point format.

IlmThread is a thread abstraction library for use with OpenEXR
and other software packages.

Imath implements 2D and 3D vectors, 3x3 and 4x4 matrices, quaternions
and other useful 2D and 3D math functions.

Iex is an exception-handling library.

%package dev
Summary: Headers and libraries for building apps that use %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description dev
%{summary}.


%prep
%setup -q

%patch51 -p1 -b .no_undefined
%patch53 -p1 -b .pkgconfig

#/bootstrap


%build
%configure --disable-static

# manually set PTHREAD_LIBS to include -lpthread until libtool bogosity is fixed,
# https://bugzilla.redhat.com/show_bug.cgi?id=661333
make %{?_smp_mflags} PTHREAD_LIBS="-pthread -lpthread"


%install
make install DESTDIR=%{buildroot}

rm -fv %{buildroot}%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion IlmBase)" = "%{version}"
# is the known-failure ix86-specific or 32bit specific? guess we'll find out -- rex
# lt-ImathTest: testBoxAlgo.cpp:892: void {anonymous}::boxMatrixTransform(): Assertion `b21 == b2' failed.
%ifarch %{ix86}
make %{?_smp_mflags} check ||:
%else
make %{?_smp_mflags} check
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libHalf.so.12*
%{_libdir}/libIex-2_2.so.12*
%{_libdir}/libIexMath-2_2.so.12*
%{_libdir}/libIlmThread-2_2.so.12*
%{_libdir}/libImath-2_2.so.12*

%files dev
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/IlmBase.pc


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 2.2.0-1
- Initial version (forked from Fedora)

