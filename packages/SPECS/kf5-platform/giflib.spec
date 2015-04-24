Summary:	Library for manipulating GIF format image files
Name:		giflib
Version:	4.1.6
Release:	11%{?dist}
License:	MIT
Group:		System Environment/Libraries
URL:		http://www.sourceforge.net/projects/%{name}/
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:	libX11-devel, libICE-devel, libSM-devel, libXt-devel
Provides:	libungif = %{version}-%{release}
Obsoletes:	libungif <= %{version}-%{release}

%description
The giflib package contains a shared library of functions for loading and
saving GIF format image files. It is API and ABI compatible with libungif,
the library which supported uncompressed GIFs while the Unisys LZW patent
was in effect.

%package devel
Summary:	Development tools for programs using the giflib library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	libungif-devel = %{version}-%{release}
Obsoletes:	libungif-devel <= %{version}-%{release}

%description devel
The giflib-devel package includes header files, libraries necessary for
developing programs which use the giflib library to load and save GIF format
image files. It contains the documentation of the giflib library, too.

%package utils
Summary:	Programs for manipulating GIF format image files
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Provides:	libungif-progs = %{version}-%{release}
Obsoletes:	libungif-progs <= %{version}-%{release}

%description utils
The giflib-utils package contains various programs for manipulating GIF
format image files. Install it if you need to manipulate GIF format image
files.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} all

# Handling of libungif compatibility
MAJOR=`echo '%{version}' | sed -e 's/\([0-9]\+\)\..*/\1/'`
%{__cc} $RPM_OPT_FLAGS -shared -Wl,-soname,libungif.so.$MAJOR -Llib/.libs -lgif -o libungif.so.%{version}

%install
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Handling of libungif compatibility
install -p -m 755 libungif.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libungif.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libungif.so.4
ln -sf libungif.so.4 $RPM_BUILD_ROOT%{_libdir}/libungif.so

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

# Remove makefile relics from documentation
rm -f doc/Makefile*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib*.so.*

%files devel
%doc doc/* util/giffiltr.c util/gifspnge.c
%{_libdir}/lib*.so
%{_includedir}/*.h

%files utils
%{_bindir}/*

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 4.1.6-1
- Initial version (forked from Fedora)

