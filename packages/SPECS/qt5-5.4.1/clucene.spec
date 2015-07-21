Summary:	A C++ port of Lucene
Name:		clucene
Version:	0.9.21b
Release:	1%{?dist}
License:	LGPLv2+ or ASL 2.0
Group:		System Environment/Libraries
URL:		http://www.sourceforge.net/projects/clucene/
Source0:	http://downloads.sourceforge.net/clucene/clucene-core-%{version}.tar.bz2

# gcc-4.8/exceptions related fix, http://bugzilla.redhat.com/998477
Patch1: clucene-core-0.9.21b-gcc48.patch

# enable reference counting (LUCENE_ENABLE_REFCOUNT) for Qt Assistant (#1128293)
Patch2: clucene-core-0.9.21b-enable-refcount.patch

# fix the soname version that ended up at 0.0.0
# This bumps the soname, but that is actually wanted because of Patch2 above.
Patch3: clucene-core-0.9.21b-fix-soversion.patch

# make tests always verbose
Patch4: clucene-core-0.9.21b-verbose-tests.patch

# fix strcpy on overlapping areas and 2 unterminated buffers
Patch5: clucene-core-0.9.21b-fix-unescaping.patch

BuildRequires:  qt5-sdk-base

%description
CLucene is a C++ port of Lucene. It is a high-performance, full-
featured text search engine written in C++. CLucene is faster than
lucene as it is written in C++.

This package contains an old and deprecated version of clucene. You
need it only if the software you are using has not been updated to
work with the newer version and the newer API.

%package core
Summary:	Core clucene module
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{name}%{?_isa} = %{version}-%{release}

%description core
The core clucene module.

This package contains an old and deprecated version of clucene-core.
You need it only if the software you are using has not been updated
to work with the newer version and the newer API.

%package core-dev
Summary:	Development files for clucene-core
Group:		Development/Libraries
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description core-dev
The clucene-core-devel package includes header files and libraries
necessary for developing programs which use clucene-core library.

This package contains an old and deprecated version of clucene-core.
You need it only if the software you are using has not been updated
to work with the newer version and the newer API.

%prep
%setup -q -n clucene-core-%{version}

%patch1 -p1 -b .gcc48
%patch2 -p1 -b .enable-refcount
%patch3 -p1 -b .fix-soversion
touch src/Makefile.in
%patch4 -p1 -b .verbose-tests
%patch5 -p1 -b .fix-unescaping

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Perform the necessary renaming according to package renaming
mkdir -p $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}/%{name}/
mv -f $RPM_BUILD_ROOT%{_includedir}/{CLucene,CLucene.h,%{name}}
mv -f $RPM_BUILD_ROOT%{_libdir}/{CLucene,%{name}}
rm -f $RPM_BUILD_ROOT%{_libdir}/libclucene.so
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -sf ../libclucene.so.*.*.* libclucene.so
popd

# Don't install any libtool .la files
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

# Fix incorrect end-of-line encoding
sed -e 's/\r//' LGPL.license > LGPL.license.eol
touch -c -r LGPL.license LGPL.license.eol
mv -f LGPL.license.eol LGPL.license

# Convert everything to UTF-8
iconv -f iso-8859-1 -t utf-8 -o README.utf8 README
touch -c -r README README.utf8
mv -f README.utf8 README

%check
make check

%post core -p /sbin/ldconfig

%postun core -p /sbin/ldconfig

%files
%doc AUTHORS COPYING HACKING README REQUESTS APACHE.license LGPL.license
# Empty package

%files core
%defattr(-,root,root,-)
%doc AUTHORS COPYING HACKING README REQUESTS APACHE.license LGPL.license
%doc doc/*.htm doc/*.jpg
%{_libdir}/libclucene.so.*

%files core-dev
%defattr(-,root,root,-)
# clucene-config.h is arch/platform specific, see RHBZ #381481
%{_libdir}/%{name}/
%{_includedir}/%{name}/

%changelog
* Mon Apr 20 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.21b-1
- Initial version (forked from Fedora)
