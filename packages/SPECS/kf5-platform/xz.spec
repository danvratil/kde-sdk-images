%global compat_ver xz-4.999.9beta

Summary:	LZMA compression utilities
Name:		xz
Version:	5.2.1
Release:	1%{?dist}

# Scripts xz{grep,diff,less,more} and symlinks (copied from gzip) are
# GPLv2+, binaries are Public Domain (linked against LGPL getopt_long but its
# OK), documentation is Public Domain.
License:	GPLv2+ and Public Domain
Group:		Applications/File
# official upstream release
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.xz
# source created as "make dist" in checked out GIT tree
Source1:	%{compat_ver}.20100401git.tar.bz2

Source100:	colorxzgrep.sh
Source101:	colorxzgrep.csh

URL:		http://tukaani.org/%{name}/
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}


%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	Public Domain

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package 	static
Summary:	Statically linked library for decoding LZMA compression
Group:		System Environment/Libraries
License:	Public Domain

%description 	static
Statically linked library for decoding files compressed with LZMA or
XZ utils.  Most users should *not* install this.

%package 	dev
Summary:	Devel libraries & headers for liblzma
Group:		Development/Libraries
License:	Public Domain
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description	dev
Devel libraries and headers for liblzma.

%prep
%setup -q -a1

for i in `find . -name config.sub`; do
  perl -pi -e "s/ppc64-\*/ppc64-\* \| ppc64p7-\*/" $i
done

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
export CFLAGS

%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

# xzgrep colorization
%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE100} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE101} %{buildroot}%{profiledir}

%find_lang %name

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%license %{_pkgdocdir}/COPYING*
%doc %{_pkgdocdir}
%exclude %_pkgdocdir/examples*
%{_bindir}/*xz*
%{_mandir}/man1/*xz*
%{profiledir}/*

%files libs
%license %{_pkgdocdir}/COPYING
%{_libdir}/lib*.so.5*

%files static
%license %{_pkgdocdir}/COPYING
%{_libdir}/liblzma.a

%files dev
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc
%doc %_pkgdocdir/examples*

%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Initial version (forked from Fedora)
