# This is stable release:
#%%global rcversion RC1
Name: pcre
Version: 8.35
Release: %{?rcversion:0.}5%{?rcversion:.%rcversion}%{?dist}
%global myversion %{version}%{?rcversion:-%rcversion}
Summary: Perl-compatible regular expression library
Group: System Environment/Libraries
License: BSD
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Upstream thinks RPATH is good idea.
Patch0: pcre-8.21-multilib.patch
# Refused by upstream, bug #675477
Patch1: pcre-8.32-refused_spelling_terminated.patch
# Do no rely on wrapping signed integer while parsing {min,max} expression,
# bug #1086630, upstream bug #1463
Patch2: pcre-8.35-Do-not-rely-on-wrapping-signed-integer-while-parsein.patch
# Fix bad starting data when char with more than one other case follows
# circumflex in multiline UTF mode, bug #1110620, upstream bug #1492,
# in upstream after 8.35
Patch3: pcre-8.35-Fix-bad-starting-data-when-char-with-more-than-one-o.patch
# Fix not including VT in starting characters for \s if pcre_study() is used,
# bug #1111045, upstream bug #1493, in upstream after 8.35
Patch4: pcre-8.35-Fix-not-including-VT-in-starting-characters-for-s.patch
# Fix character class with a literal quotation, bug #1111054,
# upstream bug #1494, in upstream after 8.35
Patch5: pcre-8.35-Fix-bad-compile-of-Qx-.-where-x-is-any-character.patch
# Fix empty-matching possessive zero-repeat groups in interpreted mode,
# bug #1119241, upstream bug #1500, in upstream after 8.35
Patch6: pcre-8.35-Fix-empty-matching-possessive-zero-repeat-groups-bug.patch
# Fix memory leaks in pcregrep, bug #1119257, upstream bug #1502,
# in upstream after 8.35
Patch7: pcre-8.35-Fixed-several-memory-leaks-in-pcregrep.patch
# Fix compiler crash for zero-repeated groups with a recursive back reference,
# bug #1119272, upstream bug #1503, in upstream after 8.35
Patch8: pcre-8.35-Fix-compiler-crash-misbehaviour-for-zero-repeated-gr.patch
# Fix compile-time loop for recursive reference within a group with an
# indefinite repeat, bug #1128577, upstream bug #1515, in upstream after 8.35
Patch9: pcre-8.35-Fix-compile-time-loop-for-recursive-reference-within.patch


BuildRequires: freedesktop-sdk-base

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package -n pcre16
Summary: PCRE 16-bit API
%description -n pcre16
%{summary}.

%package -n pcre16-dev
Summary: Development files for pcre16
Group: Development/Libraries
Requires: %{name}16%{?_isa} = %{version}-%{release}
%description -n pcre16-dev
%{summary}.

%package -n pcre32
Summary: PCRE 32-bit API
%description -n pcre32
%{summary}.

%package -n pcre32-dev
Summary: Development files for pcre32
Group: Development/Libraries
Requires: %{name}32%{?_isa} = %{version}-%{release}
%description -n pcre32-dev
%{summary}.

%package doc
Summary: API documentation and user manuals
%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{myversion}
# Get rid of rpath
%patch0 -p1 -b .multilib
%patch1 -p1 -b .terminated_typos
%patch2 -p1 -b .gcc49
%patch3 -p1 -b .starting_data
%patch4 -p1 -b .studied_vt
%patch5 -p1 -b .class_with_literal
%patch6 -p1 -b .empty_zero_repeat_group
%patch7 -p1 -b .pcregrep_leak
%patch8 -p1 -b .compiler_crash_zero_group
%patch9 -p1 -b .compiler_loop_recursive_reference
# Because of rpath patch
libtoolize --copy --force && autoreconf -vif
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
%configure \
    --enable-jit \
    --enable-pcretest-libreadline --enable-utf --enable-unicode-properties \
    --enable-static=no \
    --disable-cpp \
    --disable-pcre8 \
    --enable-pcre16 \
    --enable-pcre32
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

# already provided by our yocto base
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libpcre.pc
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libpcreposix.pc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS NEWS README ChangeLog
# We need at least an empty package

%files -n pcre16
%doc COPYING AUTHORS NEWS README ChangeLog
%{_libdir}/libpcre16.so.*

%files -n pcre16-dev
%doc HACKING
%{_libdir}/libpcre16.so
%{_libdir}/pkgconfig/libpcre16.pc
%{_mandir}/man3/pcre16*

%files -n pcre32
%doc COPYING AUTHORS NEWS README ChangeLog
%{_libdir}/libpcre32.so.*

%files -n pcre32-dev
%doc HACKING
%{_libdir}/libpcre32.so
%{_libdir}/pkgconfig/libpcre32.pc
%{_mandir}/man3/pcre32*

%files doc
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/pcre16_*
%exclude %{_mandir}/man3/pcre32_*

%changelog
* Tue Apr 21 2015 Daniel Vrátil <dvratil@redhat.com> - 8.35-1
- Initial version (forked from Fedora)
    - keep in sync with what's in yocto base (freedesktop-sdk-base), because
      we will use it's 8bit library
