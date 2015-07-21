%global build_jack 0

Name:           portaudio
Version:        19
Release:        1%{?dist}
Summary:        Free, cross platform, open-source, audio I/O library
Group:          System Environment/Libraries
License:        MIT
URL:            http://www.portaudio.com/
Source0:        http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
#Patch1:         portaudio-doxynodate.patch

Patch2:         portaudio-pkgconfig-alsa.patch

# Add some extra API needed by audacity
# http://audacity.googlecode.com/svn/audacity-src/trunk/lib-src/portmixer/portaudio.patch
#Patch3:         portaudio-audacity.patch

BuildRequires:  freedesktop-sdk-base
#BuildRequires:  doxygen
BuildRequires:  alsa-lib-dev
%if 0%{?build_jack}
BuildRequires:  jack-audio-connection-kit-devel
%endif

%description
PortAudio is a portable audio I/O library designed for cross-platform
support of audio. It uses a callback mechanism to request audio processing.
Audio can be generated in various formats, including 32 bit floating point,
and will be converted to the native format internally.


%package dev
Summary:        Development files for the portaudio audio I/O library
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
PortAudio is a portable audio I/O library designed for cross-platform
support of audio. It uses a callback mechanism to request audio processing.
Audio can be generated in various formats, including 32 bit floating point,
and will be converted to the native format internally.

This package contains files required to build applications that will use the
portaudio library.


%prep
%setup -q -n %{name}
#%patch1 -p1
%patch2 -p1
#%patch3 -p1
# Needed for patch3
autoreconf -i -f


%build
%configure --disable-static --enable-cxx
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' bindings/cpp/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' bindings/cpp/libtool
# no -j# because building with -j# is broken
make
# Build html devel documentation
#doxygen


%install
%make_install


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc LICENSE.txt README.txt
%{_libdir}/*.so.*

%files dev
#%doc doc/html/*
%{_includedir}/portaudiocpp/
%{_includedir}/portaudio.h
%if 0%{?build_jack}
%{_includedir}/pa_jack.h
%{_includedir}/pa_unix_oss.h
%endif
%{_includedir}/pa_linux_alsa.h
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Apr 21 2015 Daniel Vrátil <dvratil@redhat.com> - 19-1
- Initial version (forked from Fedora)
