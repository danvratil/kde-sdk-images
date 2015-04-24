#define gitdate 20120904

Name:           mesa-libGLU
Version:        9.0.0
Release:        1%{?dist}
Summary:        Mesa libGLU library

License:        MIT
URL:            http://mesa3d.org/
Source0:        ftp://ftp.freedesktop.org/pub/mesa/glu/glu-%{version}.tar.bz2
Source2:        make-git-snapshot.sh

Patch1: 0001-glu-initialize-PriorityQ-order-field-to-NULL-in-pqNe.patch
Patch2: 0002-Add-D-N-DEBUG-to-CFLAGS-dependent-on-enable-debug.patch

BuildRequires:  mesa-libGL-dev
Provides:       libGLU

%description
Mesa implementation of the standard GLU OpenGL utility API.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
#Requires:       gl-manpages
Provides:	    libGLU-dev

%description    dev
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n glu-%{?gitdate:%{gitdate}}%{?!gitdate:%{version}}
%patch1 -p1
%patch2 -p1

%build
autoreconf -v -i -f
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/man3/gl[A-Z]*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.*

%files dev
%{_includedir}/GL/glu*.h
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 9.0.0-1
- Initial version (forked from Fedora)
